# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.manufacturer.manufacturer_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Manufacturer module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKManufacturerRecord
from ramstk.models.dbtables import RAMSTKManufacturerTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateManufacturerModels:
    """Class for unit testing Manufacturer model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Manufacturer record model instance."""
        assert isinstance(test_record_model, RAMSTKManufacturerRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_manufacturer"
        assert test_record_model.manufacturer_id == 1
        assert test_record_model.cage_code == "47278"
        assert test_record_model.description == "Eaton"
        assert test_record_model.location == "Cleveland, OH"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Manufacturer table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKManufacturerTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "manufacturer_id",
        ]
        assert unit_test_table_model._tag == "manufacturer"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_manufacturer_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_manufacturer_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectManufacturer(UnitTestSelectMethods):
    """Class for unit testing Manufacturer table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKManufacturerRecord
    _tag = "manufacturer"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterManufacturer(UnitTestGetterSetterMethods):
    """Class for unit testing Manufacturer table methods that get or set."""

    __test__ = True

    _id_columns = [
        "manufacturer_id",
    ]

    _test_attr = "cage_code"
    _test_default_value = "CAGE Code"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["manufacturer_id"] == 1
        assert _attributes["cage_code"] == "47278"
        assert _attributes["description"] == "Eaton"
        assert _attributes["location"] == "Cleveland, OH"
