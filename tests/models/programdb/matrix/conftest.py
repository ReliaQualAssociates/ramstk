# -*- coding: utf-8 -*-
#
#       tests.models.programdb.matrix.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Matrix module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMatrixRecord
from ramstk.models.dbtables import RAMSTKMatrixTable
from tests import MockDAO

DESCRIPTION = "validation-requirement"


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _matrix_one = RAMSTKMatrixRecord()
    _matrix_one.revision_id = 1
    _matrix_one.matrix_id = 1
    _matrix_one.description = DESCRIPTION
    _matrix_one.column_id = 6
    _matrix_one.row_id = 3
    _matrix_one.correlation = "P"

    _matrix_two = RAMSTKMatrixRecord()
    _matrix_two.revision_id = 1
    _matrix_two.matrix_id = 2
    _matrix_two.description = DESCRIPTION
    _matrix_two.column_id = 6
    _matrix_two.row_id = 4
    _matrix_two.correlation = "C"

    dao = MockDAO()
    dao.table = [
        _matrix_one,
        _matrix_two,
    ]

    yield dao


@pytest.fixture
def test_attributes():
    """Create a dict of Matrix attributes."""
    yield {
        "revision_id": 1,
        "matrix_id": 1,
        "description": DESCRIPTION,
        "column_id": 6,
        "row_id": 3,
        "correlation": "P",
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMatrixTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_matrix_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_matrix_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_matrix")
    pub.unsubscribe(dut.do_update, "request_update_matrix")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_matrix_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_matrix")
    pub.unsubscribe(dut.do_insert, "request_insert_matrix")

    # Delete the device under test.
    del dut
