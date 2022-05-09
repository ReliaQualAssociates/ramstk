# -*- coding: utf-8 -*-
#
#       tests.models.programdb.failure_definition.conftest.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureDefinitionRecord
from ramstk.models.dbtables import RAMSTKFailureDefinitionTable
from tests import MockDAO


@pytest.fixture
def mock_dao(monkeypatch):
    """Create a mock database table."""
    _definition_1 = RAMSTKFailureDefinitionRecord()
    _definition_1.revision_id = 1
    _definition_1.function_id = 1
    _definition_1.definition_id = 1
    _definition_1.definition = "Mock Failure Definition 1"

    _definition_2 = RAMSTKFailureDefinitionRecord()
    _definition_2.revision_id = 1
    _definition_1.function_id = 1
    _definition_2.definition_id = 2
    _definition_2.definition = "Mock Failure Definition 2"

    dao = MockDAO()
    dao.table = [
        _definition_1,
        _definition_2,
    ]

    yield dao


@pytest.fixture(scope="function")
def test_attributes():
    """Create a dict of Failure Definition attributes."""
    yield {
        "revision_id": 1,
        "function_id": 1,
        "definition_id": 1,
        "definition": "Failure Definition",
    }


@pytest.fixture(scope="class")
def test_table_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFailureDefinitionTable()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_definition")
    pub.unsubscribe(dut.do_update, "request_update_definition")
    pub.unsubscribe(dut.do_get_tree, "request_get_definition_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_definition")
    pub.unsubscribe(dut.do_insert, "request_insert_definition")

    # Delete the device under test.
    del dut
