# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.fmea.fmea_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.models import RAMSTKFMEAView


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFMEAView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_modes")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_causes")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_controls")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_actions")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_viewmodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_viewmodel):
        """should return a view manager instance."""
        assert isinstance(test_viewmodel, RAMSTKFMEAView)
        assert isinstance(test_viewmodel.tree, Tree)
        assert isinstance(test_viewmodel.dao, BaseDatabase)
        assert test_viewmodel._tag == "fmea"
        assert test_viewmodel._root == 0
        assert test_viewmodel._revision_id == 0
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_mode")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_cause")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_control")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_action")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_modes")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_causes")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_controls")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_actions")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mode")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_cause")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_control")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_action")
