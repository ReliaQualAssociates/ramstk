# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.subcategory.subcategory_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing SubCategory module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSubCategoryRecord
from ramstk.models.dbtables import RAMSTKSubCategoryTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateSubcategoryModels:
    """Class for unit testing Subcategory model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Subcategory record model instance."""
        assert isinstance(test_record_model, RAMSTKSubCategoryRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_subcategory"
        assert test_record_model.category_id == 1
        assert test_record_model.subcategory_id == 1
        assert test_record_model.description == "Linear"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Subcategory table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKSubCategoryTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "category_id",
            "subcategory_id",
        ]
        assert unit_test_table_model._tag == "subcategory"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_subcategory_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_subcategory_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectSubcategory(UnitTestSelectMethods):
    """Class for unit testing Subcategory table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKSubCategoryRecord
    _tag = "subcategory"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterSubcategory(UnitTestGetterSetterMethods):
    """Class for unit testing Subcategory table methods that get or set."""

    __test__ = True

    _id_columns = [
        "category_id",
        "subcategory_id",
    ]

    _test_attr = "description"
    _test_default_value = "Subcategory Description"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["category_id"] == 1
        assert _attributes["subcategory_id"] == 1
        assert _attributes["description"] == "Linear"
