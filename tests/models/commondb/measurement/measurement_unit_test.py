# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.measurement.measurement_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Measurement module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMeasurementRecord
from ramstk.models.dbtables import RAMSTKMeasurementTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMeasurementModels:
    """Class for unit testing Measurement model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Measurement record model instance."""
        assert isinstance(test_record_model, RAMSTKMeasurementRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_measurement"
        assert test_record_model.measurement_id == 1
        assert test_record_model.measurement_type == "unit"
        assert test_record_model.code == "CBT"
        assert test_record_model.description == "Cubic Butt Ton"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Measurement table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMeasurementTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "measurement_id",
        ]
        assert unit_test_table_model._tag == "measurement"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_measurement_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_measurement_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMeasurement(UnitTestSelectMethods):
    """Class for unit testing Measurement table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMeasurementRecord
    _tag = "measurement"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMeasurement(UnitTestGetterSetterMethods):
    """Class for unit testing Measurement table methods that get or set."""

    __test__ = True

    _id_columns = [
        "measurement_id",
    ]

    _test_attr = "code"
    _test_default_value = "Measurement Code"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["measurement_id"] == 1
        assert _attributes["measurement_type"] == "unit"
        assert _attributes["code"] == "CBT"
        assert _attributes["description"] == "Cubic Butt Ton"
