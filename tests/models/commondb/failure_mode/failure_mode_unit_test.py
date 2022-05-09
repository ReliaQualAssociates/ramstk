# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.failure_mode.failure_mode_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Failure Mode module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureModeRecord
from ramstk.models.dbtables import RAMSTKFailureModeTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateFailureModeModels:
    """Class for unit testing Failure Mode model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Failure Mode record model instance."""
        assert isinstance(test_record_model, RAMSTKFailureModeRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_failure_mode"
        assert test_record_model.category_id == 1
        assert test_record_model.subcategory_id == 1
        assert test_record_model.mode_id == 1
        assert test_record_model.description == "Short (pin-to-pin)"
        assert test_record_model.mode_ratio == 0.65
        assert test_record_model.source == "FMD-97"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Failure Mode table model."""
        assert isinstance(unit_test_table_model, RAMSTKFailureModeTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "category_id",
            "subcategory_id",
            "mode_id",
        ]
        assert unit_test_table_model._tag == "failure_mode"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_failure_mode_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_failure_mode_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectFailureMode(UnitTestSelectMethods):
    """Class for unit testing Failure Mode table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKFailureModeRecord
    _tag = "failure_mode"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterFailureMode(UnitTestGetterSetterMethods):
    """Class for unit testing Failure Mode table methods that get or set."""

    __test__ = True

    _id_columns = [
        "category_id",
        "subcategory_id",
        "mode_id",
    ]

    _test_attr = "mode_ratio"
    _test_default_value = 1.0

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["category_id"] == 1
        assert _attributes["subcategory_id"] == 1
        assert _attributes["mode_id"] == 1
        assert _attributes["description"] == "Short (pin-to-pin)"
        assert _attributes["mode_ratio"] == 0.65
        assert _attributes["source"] == "FMD-97"
