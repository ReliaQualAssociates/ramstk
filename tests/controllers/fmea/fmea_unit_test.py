# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.pof.pof_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFMEA
from ramstk.db.base import BaseDatabase


@pytest.fixture(scope="function")
def test_datamanager():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFMEA()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_mode_tree, "succeed_retrieve_modes")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_cause_tree, "succeed_retrieve_causes")
    pub.unsubscribe(dut.do_set_control_tree, "succeed_retrieve_controls")
    pub.unsubscribe(dut.do_set_action_tree, "succeed_retrieve_actions")
    pub.unsubscribe(dut.do_set_mode_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_cause_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_control_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_action_tree, "succeed_delete_action")
    pub.unsubscribe(dut._on_insert, "succeed_insert_mode")
    pub.unsubscribe(dut._on_insert, "succeed_insert_mechanism")
    pub.unsubscribe(dut._on_insert, "succeed_insert_cause")
    pub.unsubscribe(dut._on_insert, "succeed_insert_control")
    pub.unsubscribe(dut._on_insert, "succeed_insert_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a FMEA data manager instance."""
        assert isinstance(test_datamanager, dmFMEA)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, BaseDatabase)
        assert test_datamanager._tag == "fmea"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert isinstance(test_datamanager._mode_tree, Tree)
        assert isinstance(test_datamanager._mechanism_tree, Tree)
        assert isinstance(test_datamanager._cause_tree, Tree)
        assert isinstance(test_datamanager._control_tree, Tree)
        assert isinstance(test_datamanager._action_tree, Tree)

        assert pub.isSubscribed(
            test_datamanager.do_set_mode_tree, "succeed_retrieve_modes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mechanism_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_cause_tree, "succeed_retrieve_causes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_control_tree, "succeed_retrieve_controls"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_action_tree, "succeed_retrieve_actions"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mode_tree, "succeed_delete_mode"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mechanism_tree, "succeed_delete_mechanism"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_cause_tree, "succeed_delete_cause"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_control_tree, "succeed_delete_control"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_action_tree, "succeed_delete_action"
        )
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_mode")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_cause")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_control")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_action")
