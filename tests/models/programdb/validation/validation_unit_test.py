# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.validation.validation_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models."""

# Standard Library Imports
from datetime import date, datetime, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKValidationRecord
from ramstk.models.dbtables import RAMSTKValidationTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateValidationModels:
    """Class for unit testing Validation model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Validation record model instance."""
        assert isinstance(test_record_model, RAMSTKValidationRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_validation"
        assert test_record_model.revision_id == 1
        assert test_record_model.acceptable_maximum == 30.0
        assert test_record_model.acceptable_mean == 20.0
        assert test_record_model.acceptable_minimum == 10.0
        assert test_record_model.acceptable_variance == 0.0
        assert test_record_model.confidence == 95.0
        assert test_record_model.cost_average == 0.0
        assert test_record_model.cost_ll == 0.0
        assert test_record_model.cost_maximum == 0.0
        assert test_record_model.cost_mean == 0.0
        assert test_record_model.cost_minimum == 0.0
        assert test_record_model.cost_ul == 0.0
        assert test_record_model.cost_variance == 0.0
        assert test_record_model.date_end == datetime.strftime(
            date.today() + timedelta(days=30), "%Y-%m-%d"
        )
        assert test_record_model.date_start == datetime.strftime(
            date.today(), "%Y-%m-%d"
        )
        assert test_record_model.description == ""
        assert test_record_model.measurement_unit == 0
        assert test_record_model.name == "PRF-0001"
        assert test_record_model.status == 0.0
        assert test_record_model.task_type == 0
        assert test_record_model.task_specification == ""
        assert test_record_model.time_average == 0.0
        assert test_record_model.time_ll == 0.0
        assert test_record_model.time_maximum == 0.0
        assert test_record_model.time_mean == 0.0
        assert test_record_model.time_minimum == 0.0
        assert test_record_model.time_ul == 0.0
        assert test_record_model.time_variance == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Validation table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKValidationTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert unit_test_table_model._db_id_colname == "fld_validation_id"
        assert unit_test_table_model._db_tablename == "ramstk_validation"
        assert unit_test_table_model._tag == "validation"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_validation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_validation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_validation_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_validation_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_validation_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_validation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_validation"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_plan, "request_calculate_plan"
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_calculate_task,
            "request_calculate_validation_task",
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_calculate_all_tasks,
            "request_calculate_all_validation_tasks",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectValidation(UnitTestSelectMethods):
    """Class for unit testing Validation table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKValidationRecord
    _tag = "validation"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertValidation(UnitTestInsertMethods):
    """Class for unit testing Validation table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKValidationRecord
    _tag = "validation"

    @pytest.mark.skip(reason="Validation records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Validation records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteValidation(UnitTestDeleteMethods):
    """Class for unit testing Validation table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKValidationRecord
    _tag = "validation"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterTestMethod(UnitTestGetterSetterMethods):
    """Class for unit testing Test Method table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "validation_id",
    ]

    _test_attr = "time_variance"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["acceptable_maximum"] == 30.0
        assert _attributes["acceptable_mean"] == 20.0
        assert _attributes["acceptable_minimum"] == 10.0
        assert _attributes["acceptable_variance"] == 0.0
        assert _attributes["confidence"] == 95.0
        assert _attributes["cost_average"] == 0.0
        assert _attributes["cost_ll"] == 0.0
        assert _attributes["cost_maximum"] == 0.0
        assert _attributes["cost_mean"] == 0.0
        assert _attributes["cost_minimum"] == 0.0
        assert _attributes["cost_ul"] == 0.0
        assert _attributes["cost_variance"] == 0.0
        assert _attributes["date_end"] == datetime.strftime(
            date.today() + timedelta(days=30), "%Y-%m-%d"
        )
        assert _attributes["date_start"] == datetime.strftime(date.today(), "%Y-%m-%d")
        assert _attributes["description"] == ""
        assert _attributes["measurement_unit"] == 0
        assert _attributes["name"] == "PRF-0001"
        assert _attributes["status"] == 0.0
        assert _attributes["task_type"] == 0
        assert _attributes["task_specification"] == ""
        assert _attributes["time_average"] == 0.0
        assert _attributes["time_ll"] == 0.0
        assert _attributes["time_maximum"] == 0.0
        assert _attributes["time_mean"] == 0.0
        assert _attributes["time_minimum"] == 0.0
        assert _attributes["time_ul"] == 0.0
        assert _attributes["time_variance"] == 0.0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestValidationAnalysisMethods:
    """Class for testing Validation analytical methods."""

    @pytest.mark.unit
    def test_do_select_assessment_targets(self, test_attributes, unit_test_table_model):
        """Should return a pandas DataFrame() containing assessment target values."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _targets = unit_test_table_model._do_select_assessment_targets()

        assert isinstance(_targets, pd.DataFrame)
        assert (
            _targets.loc[pd.to_datetime(date.today() + timedelta(30)), "lower"] == 10.0
        )
        assert (
            _targets.loc[pd.to_datetime(date.today() + timedelta(30)), "mean"] == 20.0
        )
        assert (
            _targets.loc[pd.to_datetime(date.today() + timedelta(30)), "upper"] == 30.0
        )

    @pytest.mark.unit
    def test_do_calculate_task(self, test_attributes, unit_test_table_model):
        """Should calculate the validation task time and cost."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _validation = unit_test_table_model.do_select(1)
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        unit_test_table_model.do_update(1)

        unit_test_table_model._do_calculate_task(node_id=1)

        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_ll == pytest.approx(11.86684674)
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_mean == pytest.approx(21.66666667)
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].time_ul == pytest.approx(31.46648659)
        assert (
            unit_test_table_model.tree.get_node(1).data["validation"].time_variance
            == 25.0
        )
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_ll == pytest.approx(1659.34924016)
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_mean == pytest.approx(2525.0)
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_ul == pytest.approx(3390.65075984)
        assert unit_test_table_model.tree.get_node(1).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)
