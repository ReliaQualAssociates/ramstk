# -*- coding: utf-8 -*-
#
#       tests.models.programdb.fmea.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK FMEA module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbviews import RAMSTKFMEAView


@pytest.fixture(scope="class")
def test_view_model(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFMEAView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut
