# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.condition.condition_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Condition module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKConditionRecord
from ramstk.models.dbtables import RAMSTKConditionTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateCategory:
    """Class for unit testing Condition model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Condition record model instance."""
        assert isinstance(test_record_model, RAMSTKConditionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_condition"
        assert test_record_model.condition_id == 1
        assert test_record_model.condition_type == "operating"
        assert test_record_model.description == "Cavitation"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Condition table model."""
        assert isinstance(unit_test_table_model, RAMSTKConditionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "condition_id",
        ]
        assert unit_test_table_model._tag == "condition"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_condition_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_condition_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectCondition(UnitTestSelectMethods):
    """Class for unit testing Condition table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKConditionRecord
    _tag = "condition"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterCondition(UnitTestGetterSetterMethods):
    """Class for unit testing Condition table methods that get or set."""

    __test__ = True

    _id_columns = [
        "condition_id",
    ]

    _test_attr = "condition_type"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["condition_id"] == 1
        assert _attributes["condition_type"] == "operating"
        assert _attributes["description"] == "Cavitation"
