# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.usage_profile.usage_profile_unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Usage Profile module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmUsageProfile
from ramstk.db.base import BaseDatabase


@pytest.fixture(scope="function")
def test_datamanager():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmUsageProfile()
    # dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_insert, "succeed_insert_environment")
    pub.unsubscribe(dut.on_insert, "succeed_insert_mission")
    pub.unsubscribe(dut.on_insert, "succeed_insert_mission_phase")
    pub.unsubscribe(dut.do_set_environment_tree, "succeed_retrieve_environments")
    pub.unsubscribe(dut.do_set_mission_tree, "succeed_retrieve_missions")
    pub.unsubscribe(dut.do_set_mission_phase_tree, "succeed_retrieve_mission_phases")
    pub.unsubscribe(dut.do_set_environment_tree, "succeed_delete_environment")
    pub.unsubscribe(dut.do_set_mission_tree, "succeed_delete_mission")
    pub.unsubscribe(dut.do_set_mission_phase_tree, "succeed_delete_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager(self, test_datamanager):
        """__init__() should return a Revision data manager."""
        assert isinstance(test_datamanager, dmUsageProfile)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, BaseDatabase)
        assert test_datamanager._tag == "usage_profiles"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.on_insert, "succeed_insert_environment"
        )
        assert pub.isSubscribed(test_datamanager.on_insert, "succeed_insert_mission")
        assert pub.isSubscribed(
            test_datamanager.on_insert, "succeed_insert_mission_phase"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_environment_tree, "succeed_retrieve_environments"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mission_tree, "succeed_retrieve_missions"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mission_phase_tree,
            "succeed_retrieve_mission_phases",
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_environment_tree, "succeed_delete_environment"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mission_tree, "succeed_delete_mission"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mission_phase_tree, "succeed_delete_mission_phase"
        )
