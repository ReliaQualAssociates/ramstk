# -*- coding: utf-8 -*-
#
#       tests.models.programdb.pof.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK PoF module test fixtures."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKMechanismRecord,
    RAMSTKOpLoadRecord,
    RAMSTKOpStressRecord,
    RAMSTKTestMethodRecord,
)
from ramstk.models.dbtables import (
    RAMSTKMechanismTable,
    RAMSTKOpLoadTable,
    RAMSTKOpStressTable,
    RAMSTKTestMethodTable,
)
from ramstk.models.dbviews import RAMSTKPoFView
from tests import MockDAO


@pytest.fixture(scope="function")
def unit_test_view_model():
    """Get a table model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKPoFView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_test_method")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_test_method")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_test_method")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def integration_test_view_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKPoFView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_test_method")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_test_method")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_test_method")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_mechanism(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMechanismTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opload(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpLoadTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_opstress(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpStressTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "opload_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_method(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKTestMethodTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "opload_id": 3,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_test_method")
    pub.unsubscribe(dut.do_insert, "request_insert_test_method")

    # Delete the device under test.
    del dut
