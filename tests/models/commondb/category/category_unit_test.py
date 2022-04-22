# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.category.category_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Category module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCategoryRecord
from ramstk.models.dbtables import RAMSTKCategoryTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateCategory:
    """Class for unit testing Category model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Category record model instance."""
        assert isinstance(test_record_model, RAMSTKCategoryRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_category"
        assert test_record_model.category_id == 1
        assert test_record_model.category_type == "hardware"
        assert test_record_model.name == "IC"
        assert test_record_model.value == 1
        assert test_record_model.description == "Integrated Circuit"
        assert test_record_model.harsh_ir_limit == 0.8
        assert test_record_model.mild_ir_limit == 0.9
        assert test_record_model.harsh_pr_limit == 1.0
        assert test_record_model.mild_pr_limit == 1.0
        assert test_record_model.harsh_vr_limit == 1.0
        assert test_record_model.mild_vr_limit == 1.0
        assert test_record_model.harsh_deltat_limit == 0.0
        assert test_record_model.mild_deltat_limit == 0.0
        assert test_record_model.harsh_maxt_limit == 125.0
        assert test_record_model.mild_maxt_limit == 125.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Category table model."""
        assert isinstance(unit_test_table_model, RAMSTKCategoryTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "category_id",
        ]
        assert unit_test_table_model._tag == "category"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_category_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_category_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectCategory(UnitTestSelectMethods):
    """Class for unit testing Category table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKCategoryRecord
    _tag = "category"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterCategory(UnitTestGetterSetterMethods):
    """Class for unit testing Category table methods that get or set."""

    __test__ = True

    _id_columns = [
        "category_id",
    ]

    _test_attr = "harsh_ir_limit"
    _test_default_value = 0.8

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["category_id"] == 1
        assert _attributes["category_type"] == "hardware"
        assert _attributes["name"] == "IC"
        assert _attributes["value"] == 1
        assert _attributes["description"] == "Integrated Circuit"
        assert _attributes["harsh_ir_limit"] == 0.8
        assert _attributes["mild_ir_limit"] == 0.9
        assert _attributes["harsh_pr_limit"] == 1.0
        assert _attributes["mild_pr_limit"] == 1.0
        assert _attributes["harsh_vr_limit"] == 1.0
        assert _attributes["mild_vr_limit"] == 1.0
        assert _attributes["harsh_deltat_limit"] == 0.0
        assert _attributes["mild_deltat_limit"] == 0.0
        assert _attributes["harsh_maxt_limit"] == 125.0
        assert _attributes["mild_maxt_limit"] == 125.0
