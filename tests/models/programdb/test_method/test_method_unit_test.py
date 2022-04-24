# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_method.method_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Test Method algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTestMethodRecord
from ramstk.models.dbtables import RAMSTKTestMethodTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateTestMethodModels:
    """Class for unit testing Test Method model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Test Method record model instance."""
        assert isinstance(test_record_model, RAMSTKTestMethodRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_test_method"
        assert test_record_model.description == "Test Test Method #1"
        assert test_record_model.boundary_conditions == "Waters"
        assert test_record_model.remarks == ""

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Test Method table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKTestMethodTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert unit_test_table_model._db_id_colname == "fld_test_method_id"
        assert unit_test_table_model._db_tablename == "ramstk_test_method"
        assert unit_test_table_model._tag == "test_method"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_test_method_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_test_method_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_test_method"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_test_method"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_test_method_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_test_method"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_test_method"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectTestMethod(UnitTestSelectMethods):
    """Class for unit testing Test Method table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKTestMethodRecord
    _tag = "test_method"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertTestMethod(UnitTestInsertMethods):
    """Class for unit testing Test Method table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKTestMethodRecord
    _tag = "test_method"

    @pytest.mark.skip(reason="Test Method records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Test Method records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteTestMethod(UnitTestDeleteMethods):
    """Class for unit testing Test Method table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKTestMethodRecord
    _tag = "test_method"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterTestMethod(UnitTestGetterSetterMethods):
    """Class for unit testing Test Method table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "opload_id",
        "test_method_id",
    ]

    _test_attr = "boundary_conditions"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test Test Method #1"
        assert _attributes["boundary_conditions"] == "Waters"
        assert _attributes["remarks"] == ""
