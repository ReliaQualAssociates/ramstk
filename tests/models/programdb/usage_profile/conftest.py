# -*- coding: utf-8 -*-
#
#       tests.models.programdb.usage_profile.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Usage Profile module test fixtures."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.dbviews import RAMSTKUsageProfileView


@pytest.fixture(scope="class")
def test_view_model():
    """Get a view model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKUsageProfileView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission_phase")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_mission_phase")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission_phase")

    # Delete the device under test.
    del dut
