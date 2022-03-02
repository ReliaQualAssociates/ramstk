# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.usage_profile.usage_profile_unit_test.py is part of The RAMSTK
#       Project
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
from ramstk.db.base import BaseDatabase
from ramstk.models.dbviews import RAMSTKUsageProfileView


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKUsageProfileView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mission_phase")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_environments")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_missions")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_mission_phases")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_environment")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_viewmodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager(self, test_viewmodel):
        """should return a view manager instance."""
        assert isinstance(test_viewmodel, RAMSTKUsageProfileView)
        assert isinstance(test_viewmodel.tree, Tree)
        assert isinstance(test_viewmodel.dao, BaseDatabase)
        assert test_viewmodel._tag == "usage_profile"
        assert test_viewmodel._root == 0
        assert test_viewmodel._revision_id == 0
        assert test_viewmodel._dic_load_functions == {
            "mission": test_viewmodel._do_load_missions,
            "mission_phase": test_viewmodel._do_load_mission_phases,
            "environment": test_viewmodel._do_load_environments,
        }
        assert isinstance(test_viewmodel._dic_trees["mission"], Tree)
        assert isinstance(test_viewmodel._dic_trees["mission_phase"], Tree)
        assert isinstance(test_viewmodel._dic_trees["environment"], Tree)
        assert test_viewmodel._lst_modules == [
            "mission",
            "mission_phase",
            "environment",
        ]
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_environment"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_mission")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_mission_phase"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_environments"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_missions")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree,
            "succeed_retrieve_mission_phases",
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_environment"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mission")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_mission_phase"
        )
