# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.hazards.hazards_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazards module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardsRecord
from ramstk.models.dbtables import RAMSTKHazardsTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateHazardsModels:
    """Class for unit testing Hazards model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Hazards record model instance."""
        assert isinstance(test_record_model, RAMSTKHazardsRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_hazards"
        assert test_record_model.hazard_id == 1
        assert test_record_model.hazard_category == "Common Causes"
        assert test_record_model.hazard_subcategory == "Fire"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Hazards table model."""
        assert isinstance(unit_test_table_model, RAMSTKHazardsTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "hazard_id",
        ]
        assert unit_test_table_model._tag == "hazards"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_hazards_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_hazards_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectHazards(UnitTestSelectMethods):
    """Class for unit testing Group table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKHazardsRecord
    _tag = "hazards"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterHazards(UnitTestGetterSetterMethods):
    """Class for unit testing Hazards table methods that get or set."""

    __test__ = True

    _id_columns = [
        "hazard_id",
    ]

    _test_attr = "hazard_category"
    _test_default_value = "Hazard Category"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["hazard_id"] == 1
        assert _attributes["hazard_category"] == "Common Causes"
        assert _attributes["hazard_subcategory"] == "Fire"
