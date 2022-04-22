# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.rpn.rpn_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing RPN module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRPNRecord
from ramstk.models.dbtables import RAMSTKRPNTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateRPNModels:
    """Class for unit testing RPN model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return an RPN record model instance."""
        assert isinstance(test_record_model, RAMSTKRPNRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_rpn"
        assert test_record_model.rpn_id == 1
        assert test_record_model.rpn_type == "severity"
        assert test_record_model.name == "Very Minor"
        assert test_record_model.value == 1
        assert (
            test_record_model.description
            == "System operable with minimal interference."
        )

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return an RPN table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKRPNTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "rpn_id",
        ]
        assert unit_test_table_model._tag == "rpn"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_rpn_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_rpn_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectRPN(UnitTestSelectMethods):
    """Class for unit testing RPN table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKRPNRecord
    _tag = "rpn"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterRPN(UnitTestGetterSetterMethods):
    """Class for unit testing RPN table methods that get or set."""

    __test__ = True

    _id_columns = [
        "rpn_id",
    ]

    _test_attr = "value"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["rpn_id"] == 1
        assert _attributes["rpn_type"] == "severity"
        assert _attributes["name"] == "Very Minor"
        assert _attributes["value"] == 1
        assert (
            _attributes["description"] == "System operable with minimal interference."
        )
