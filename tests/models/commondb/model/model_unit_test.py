# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.model.model_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Model module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModelRecord
from ramstk.models.dbtables import RAMSTKModelTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateModelModels:
    """Class for unit testing Model model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Model record model instance."""
        assert isinstance(test_record_model, RAMSTKModelRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_model"
        assert test_record_model.model_id == 1
        assert test_record_model.model_type == "damage"
        assert test_record_model.description == "Trump, Donald"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Model table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKModelTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "model_id",
        ]
        assert unit_test_table_model._tag == "model"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_model_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_model_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectModel(UnitTestSelectMethods):
    """Class for unit testing Model table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKModelRecord
    _tag = "model"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterModel(UnitTestGetterSetterMethods):
    """Class for unit testing Model table methods that get or set."""

    __test__ = True

    _id_columns = [
        "model_id",
    ]

    _test_attr = "model_type"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["model_id"] == 1
        assert _attributes["model_type"] == "damage"
        assert _attributes["description"] == "Trump, Donald"
