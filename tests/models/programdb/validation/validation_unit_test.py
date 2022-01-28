# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.validation.validation_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models."""

# Standard Library Imports
from datetime import date, datetime, timedelta

# Third Party Imports
import pandas as pd
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKValidationRecord, RAMSTKValidationTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKValidationTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_validation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_validation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_validation")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_validation")
    pub.unsubscribe(dut.do_update, "request_update_validation")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_validation_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_validation")
    pub.unsubscribe(dut.do_insert, "request_insert_validation")
    pub.unsubscribe(dut.do_calculate_plan, "request_calculate_plan")
    pub.unsubscribe(dut._do_calculate_task, "request_calculate_validation_task")
    pub.unsubscribe(
        dut._do_calculate_all_tasks, "request_calculate_all_validation_tasks"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKValidationRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_validation"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.acceptable_maximum == 30.0
        assert test_recordmodel.acceptable_mean == 20.0
        assert test_recordmodel.acceptable_minimum == 10.0
        assert test_recordmodel.acceptable_variance == 0.0
        assert test_recordmodel.confidence == 95.0
        assert test_recordmodel.cost_average == 0.0
        assert test_recordmodel.cost_ll == 0.0
        assert test_recordmodel.cost_maximum == 0.0
        assert test_recordmodel.cost_mean == 0.0
        assert test_recordmodel.cost_minimum == 0.0
        assert test_recordmodel.cost_ul == 0.0
        assert test_recordmodel.cost_variance == 0.0
        assert test_recordmodel.date_end == datetime.strftime(
            date.today() + timedelta(days=30), "%Y-%m-%d"
        )
        assert test_recordmodel.date_start == datetime.strftime(
            date.today(), "%Y-%m-%d"
        )
        assert test_recordmodel.description == ""
        assert test_recordmodel.measurement_unit == 0
        assert test_recordmodel.name == "PRF-0001"
        assert test_recordmodel.status == 0.0
        assert test_recordmodel.task_type == 0
        assert test_recordmodel.task_specification == ""
        assert test_recordmodel.time_average == 0.0
        assert test_recordmodel.time_ll == 0.0
        assert test_recordmodel.time_maximum == 0.0
        assert test_recordmodel.time_mean == 0.0
        assert test_recordmodel.time_minimum == 0.0
        assert test_recordmodel.time_ul == 0.0
        assert test_recordmodel.time_variance == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKValidationTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert test_tablemodel._db_id_colname == "fld_validation_id"
        assert test_tablemodel._db_tablename == "ramstk_validation"
        assert test_tablemodel._tag == "validation"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_validation")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_validations"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_validation_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_validation_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_validation_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_validation")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_validation")
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_plan, "request_calculate_plan"
        )
        assert pub.isSubscribed(
            test_tablemodel._do_calculate_task, "request_calculate_validation_task"
        )
        assert pub.isSubscribed(
            test_tablemodel._do_calculate_all_tasks,
            "request_calculate_all_validation_tasks",
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["validation"],
            RAMSTKValidationRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _validation = test_tablemodel.do_select(1)

        assert isinstance(_validation, RAMSTKValidationRecord)
        assert _validation.acceptable_maximum == 30.0
        assert _validation.name == "PRF-0001"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKValidationRecord)
        assert _new_record.revision_id == 1
        assert _new_record.validation_id == 4

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_attributes["parent_id"] = 0
        test_attributes["record_id"] = 0
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["validation"], RAMSTKValidationRecord
        )
        assert test_tablemodel.tree.get_node(4).data["validation"].validation_id == 4
        assert (
            test_tablemodel.tree.get_node(4).data["validation"].name
            == "New Validation Task"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(test_tablemodel.last_id)

        assert test_tablemodel.last_id == 2


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

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

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("validation_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["time_variance"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("validation_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["time_variance"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("validation_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_select_assessment_targets(self, test_attributes, test_tablemodel):
        """should return a pandas DataFrame() containing assessment target values."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _targets = test_tablemodel._do_select_assessment_targets()

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
    def test_do_calculate_task(self, test_attributes, test_tablemodel):
        """should calculate the validation task time and cost."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _validation = test_tablemodel.do_select(1)
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        test_tablemodel.do_update(1)

        test_tablemodel._do_calculate_task(node_id=1)

        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_ll == pytest.approx(11.86684674)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_mean == pytest.approx(21.66666667)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_ul == pytest.approx(31.46648659)
        assert test_tablemodel.tree.get_node(1).data["validation"].time_variance == 25.0
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_ll == pytest.approx(1659.34924016)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_mean == pytest.approx(2525.0)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_ul == pytest.approx(3390.65075984)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)
