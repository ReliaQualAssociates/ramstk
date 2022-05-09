# -*- coding: utf-8 -*-
#
#       tests.models.programdb.pof.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK PoF module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbviews import RAMSTKPoFView


@pytest.fixture(scope="class")
def test_view_model(test_program_dao):
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
