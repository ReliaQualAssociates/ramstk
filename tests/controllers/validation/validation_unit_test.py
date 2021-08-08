# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.validation.validation_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKValidation
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmValidation
from ramstk.models.programdb import RAMSTKValidation


@pytest.fixture
def mock_program_dao(monkeypatch):
    _validation_1 = MockRAMSTKValidation()
    _validation_1.revision_id = 1
    _validation_1.validation_id = 1
    _validation_1.acceptable_maximum = 30.0
    _validation_1.acceptable_mean = 20.0
    _validation_1.acceptable_minimum = 10.0
    _validation_1.acceptable_variance = 0.0
    _validation_1.confidence = 95.0
    _validation_1.cost_average = 0.0
    _validation_1.cost_ll = 0.0
    _validation_1.cost_maximum = 0.0
    _validation_1.cost_mean = 0.0
    _validation_1.cost_minimum = 0.0
    _validation_1.cost_ul = 0.0
    _validation_1.cost_variance = 0.0
    _validation_1.date_end = date.today() + timedelta(days=30)
    _validation_1.date_start = date.today()
    _validation_1.description = ""
    _validation_1.measurement_unit = 0
    _validation_1.name = "PRF-0001"
    _validation_1.status = 0.0
    _validation_1.task_type = 0
    _validation_1.task_specification = ""
    _validation_1.time_average = 0.0
    _validation_1.time_ll = 0.0
    _validation_1.time_maximum = 0.0
    _validation_1.time_mean = 0.0
    _validation_1.time_minimum = 0.0
    _validation_1.time_ul = 0.0
    _validation_1.time_variance = 0.0

    _validation_2 = MockRAMSTKValidation()
    _validation_2.revision_id = 1
    _validation_2.validation_id = 2
    _validation_2.acceptable_maximum = 30.0
    _validation_2.acceptable_mean = 20.0
    _validation_2.acceptable_minimum = 10.0
    _validation_2.acceptable_variance = 0.0
    _validation_2.confidence = 95.0
    _validation_2.cost_average = 0.0
    _validation_2.cost_ll = 0.0
    _validation_2.cost_maximum = 0.0
    _validation_2.cost_mean = 0.0
    _validation_2.cost_minimum = 0.0
    _validation_2.cost_ul = 0.0
    _validation_2.cost_variance = 0.0
    _validation_2.date_end = date.today() + timedelta(days=20)
    _validation_2.date_start = date.today() - timedelta(days=10)
    _validation_2.description = ""
    _validation_2.measurement_unit = 0
    _validation_2.name = ""
    _validation_2.status = 0.0
    _validation_2.task_type = 5
    _validation_2.task_specification = ""
    _validation_2.time_average = 0.0
    _validation_2.time_ll = 0.0
    _validation_2.time_maximum = 0.0
    _validation_2.time_mean = 0.0
    _validation_2.time_minimum = 0.0
    _validation_2.time_ul = 0.0
    _validation_2.time_variance = 0.0

    _validation_3 = MockRAMSTKValidation()
    _validation_3.revision_id = 1
    _validation_3.validation_id = 3
    _validation_3.acceptable_maximum = 30.0
    _validation_3.acceptable_mean = 20.0
    _validation_3.acceptable_minimum = 10.0
    _validation_3.acceptable_variance = 0.0
    _validation_3.confidence = 95.0
    _validation_3.cost_average = 0.0
    _validation_3.cost_ll = 0.0
    _validation_3.cost_maximum = 0.0
    _validation_3.cost_mean = 0.0
    _validation_3.cost_minimum = 0.0
    _validation_3.cost_ul = 0.0
    _validation_3.cost_variance = 0.0
    _validation_3.date_end = date.today() + timedelta(days=30)
    _validation_3.date_start = date.today()
    _validation_3.description = ""
    _validation_3.measurement_unit = 0
    _validation_3.name = ""
    _validation_3.status = 0.0
    _validation_3.task_type = 5
    _validation_3.task_specification = ""
    _validation_3.time_average = 20.0
    _validation_3.time_ll = 19.0
    _validation_3.time_maximum = 40.0
    _validation_3.time_mean = 34.0
    _validation_3.time_minimum = 12.0
    _validation_3.time_ul = 49.0
    _validation_3.time_variance = 0.0

    DAO = MockDAO()
    DAO.table = [
        _validation_1,
        _validation_2,
        _validation_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "validation_id": 1,
        "name": "New Validation Task",
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmValidation()
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
    pub.unsubscribe(dut._do_calculate_all_tasks, "request_calculate_validation_tasks")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a table manager instance."""
        assert isinstance(test_datamanager, dmValidation)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._db_id_colname == "fld_validation_id"
        assert test_datamanager._db_tablename == "ramstk_validation"
        assert test_datamanager._tag == "validation"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_validation")
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_validation"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_validation_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_validation_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_validation_attributes"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_validation")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_validation")
        assert pub.isSubscribed(
            test_datamanager.do_calculate_plan, "request_calculate_plan"
        )
        assert pub.isSubscribed(
            test_datamanager._do_calculate_task, "request_calculate_validation_task"
        )
        assert pub.isSubscribed(
            test_datamanager._do_calculate_all_tasks,
            "request_calculate_validation_tasks",
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with DB records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["validation"], MockRAMSTKValidation
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return the record for the passed record ID."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _validation = test_datamanager.do_select(1)

        assert isinstance(_validation, MockRAMSTKValidation)
        assert _validation.acceptable_maximum == 30.0
        assert _validation.name == "PRF-0001"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """should return None when a non-existent record ID is requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_datamanager):
        """should return a new record instance with ID fields populated."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _new_record = test_datamanager.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKValidation)
        assert _new_record.revision_id == 1
        assert _new_record.validation_id == 4

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a new record to the records tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(4).data["validation"], RAMSTKValidation
        )
        assert test_datamanager.tree.get_node(4).data["validation"].validation_id == 4
        assert (
            test_datamanager.tree.get_node(4).data["validation"].name
            == "New Validation Task"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 2


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_select_assessment_targets(self, test_attributes, test_datamanager):
        """should return a pandas DataFrame() containing assessment target values."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _targets = test_datamanager._do_select_assessment_targets()

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
    def test_do_calculate_task(self, test_attributes, test_datamanager):
        """should calculate the validation task time and cost."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _validation = test_datamanager.do_select(1)
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        test_datamanager.do_update(1, table="validation")

        test_datamanager._do_calculate_task(node_id=1)

        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].time_ll == pytest.approx(11.86684674)
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].time_mean == pytest.approx(21.66666667)
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].time_ul == pytest.approx(31.46648659)
        assert (
            test_datamanager.tree.get_node(1).data["validation"].time_variance == 25.0
        )
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].cost_ll == pytest.approx(1659.34924016)
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].cost_mean == pytest.approx(2525.0)
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].cost_ul == pytest.approx(3390.65075984)
        assert test_datamanager.tree.get_node(1).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)
