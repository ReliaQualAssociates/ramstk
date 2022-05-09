# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.type.type_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Type module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKTypeRecord
from ramstk.models.dbtables import RAMSTKTypeTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateTypeModels:
    """Class for unit testing Type model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Type record model instance."""
        assert isinstance(test_record_model, RAMSTKTypeRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_type"
        assert test_record_model.type_id == 1
        assert test_record_model.type_type == "incident"
        assert test_record_model.code == "PLN"
        assert test_record_model.description == "Planning"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Type table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKTypeTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "type_id",
        ]
        assert unit_test_table_model._tag == "type"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_type_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_type_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectType(UnitTestSelectMethods):
    """Class for unit testing Type table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKTypeRecord
    _tag = "type"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterType(UnitTestGetterSetterMethods):
    """Class for unit testing Type table methods that get or set."""

    __test__ = True

    _id_columns = [
        "type_id",
    ]

    _test_attr = "code"
    _test_default_value = "Type Code"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["type_id"] == 1
        assert _attributes["type_type"] == "incident"
        assert _attributes["code"] == "PLN"
        assert _attributes["description"] == "Planning"
