# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.group.group_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Group module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKGroupRecord
from ramstk.models.dbtables import RAMSTKGroupTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateGroupModels:
    """Class for unit testing Group model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Group record model instance."""
        assert isinstance(test_record_model, RAMSTKGroupRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_group"
        assert test_record_model.group_id == 1
        assert test_record_model.group_type == "work"
        assert test_record_model.description == "Engineering, RMS"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Group table model."""
        assert isinstance(unit_test_table_model, RAMSTKGroupTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "group_id",
        ]
        assert unit_test_table_model._tag == "group"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_group_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_group_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectGroup(UnitTestSelectMethods):
    """Class for unit testing Group table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKGroupRecord
    _tag = "group"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterGroup(UnitTestGetterSetterMethods):
    """Class for unit testing Group table methods that get or set."""

    __test__ = True

    _id_columns = [
        "group_id",
    ]

    _test_attr = "group_type"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["group_id"] == 1
        assert _attributes["group_type"] == "work"
        assert _attributes["description"] == "Engineering, RMS"
