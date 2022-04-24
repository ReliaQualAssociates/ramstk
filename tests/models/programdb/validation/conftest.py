# -*- coding: utf-8 -*-
#
#       tests.models.programdb.validation.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Validation module test fixtures."""

# Standard Library Imports
from datetime import date, datetime, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKValidationRecord
from ramstk.models.dbtables import RAMSTKValidationTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _validation_1 = RAMSTKValidationRecord()
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
    _validation_1.date_end = datetime.strftime(
        date.today() + timedelta(days=30), "%Y-%m-%d"
    )
    _validation_1.date_start = datetime.strftime(date.today(), "%Y-%m-%d")
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

    _validation_2 = RAMSTKValidationRecord()
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
    _validation_2.date_end = datetime.strftime(
        date.today() + timedelta(days=20), "%Y-%m-%d"
    )
    _validation_2.date_start = datetime.strftime(
        date.today() - timedelta(days=10), "%Y-%m-%d"
    )
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

    _validation_3 = RAMSTKValidationRecord()
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
    _validation_3.date_end = datetime.strftime(
        date.today() + timedelta(days=30), "%Y-%m-%d"
    )
    _validation_3.date_start = datetime.strftime(date.today(), "%Y-%m-%d")
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

    dao = MockDAO()
    dao.table = [
        _validation_1,
        _validation_2,
        _validation_3,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Validation attributes."""
    yield {
        "revision_id": 1,
        "validation_id": 1,
        "acceptable_maximum": 0.0,
        "acceptable_mean": 0.0,
        "acceptable_minimum": 0.0,
        "acceptable_variance": 0.0,
        "confidence": 95.0,
        "cost_average": 0.0,
        "cost_ll": 0.0,
        "cost_maximum": 0.0,
        "cost_mean": 0.0,
        "cost_minimum": 0.0,
        "cost_ul": 0.0,
        "cost_variance": 0.0,
        "date_end": datetime.strftime(date.today() + timedelta(days=30), "%Y-%m-%d"),
        "date_start": datetime.strftime(date.today(), "%Y-%m-%d"),
        "description": "",
        "measurement_unit": 0,
        "name": "New Validation Task",
        "status": 0.0,
        "task_type": 0,
        "task_specification": "",
        "time_average": 0.0,
        "time_ll": 0.0,
        "time_maximum": 0.0,
        "time_mean": 0.0,
        "time_minimum": 0.0,
        "time_ul": 0.0,
        "time_variance": 0.0,
    }


@pytest.fixture(scope="function")
def unit_test_table_model(mock_dao):
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKValidationTable()
    dut.do_connect(mock_dao)

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
