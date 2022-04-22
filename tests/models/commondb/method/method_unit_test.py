# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.method.method_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Method module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMethodRecord
from ramstk.models.dbtables import RAMSTKMethodTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMethodModels:
    """Class for unit testing Method model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Method record model instance."""
        assert isinstance(test_record_model, RAMSTKMethodRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_method"
        assert test_record_model.method_id == 1
        assert test_record_model.method_type == "detection"
        assert test_record_model.name == "Sniff"
        assert test_record_model.description == "Smell Test"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Method table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMethodTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "method_id",
        ]
        assert unit_test_table_model._tag == "method"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_method_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_method_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMethod(UnitTestSelectMethods):
    """Class for unit testing Method table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMethodRecord
    _tag = "method"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMethod(UnitTestGetterSetterMethods):
    """Class for unit testing Method table methods that get or set."""

    __test__ = True

    _id_columns = [
        "method_id",
    ]

    _test_attr = "name"
    _test_default_value = "Method Name"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["method_id"] == 1
        assert _attributes["method_type"] == "detection"
        assert _attributes["name"] == "Sniff"
        assert _attributes["description"] == "Smell Test"
