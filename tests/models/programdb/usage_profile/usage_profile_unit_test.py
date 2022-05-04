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
from ramstk.models.db import BaseDatabase
from ramstk.models.dbviews import RAMSTKUsageProfileView


@pytest.mark.usefixtures("unit_test_view_model")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager(self, unit_test_view_model):
        """Should return a view manager instance."""
        assert isinstance(unit_test_view_model, RAMSTKUsageProfileView)
        assert isinstance(unit_test_view_model.tree, Tree)
        assert isinstance(unit_test_view_model.dao, BaseDatabase)
        assert unit_test_view_model._tag == "usage_profile"
        assert unit_test_view_model._root == 0
        assert unit_test_view_model._revision_id == 0
        assert unit_test_view_model._dic_load_functions == {
            "mission": unit_test_view_model._do_load_missions,
            "mission_phase": unit_test_view_model._do_load_mission_phases,
            "environment": unit_test_view_model._do_load_environments,
        }
        assert isinstance(unit_test_view_model._dic_trees["mission"], Tree)
        assert isinstance(unit_test_view_model._dic_trees["mission_phase"], Tree)
        assert isinstance(unit_test_view_model._dic_trees["environment"], Tree)
        assert unit_test_view_model._lst_modules == [
            "mission",
            "mission_phase",
            "environment",
        ]
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_insert_environment"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_insert_mission"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_insert_mission_phase"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_retrieve_all_environment"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_retrieve_all_mission"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree,
            "succeed_retrieve_all_mission_phase",
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_delete_environment"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_delete_mission"
        )
        assert pub.isSubscribed(
            unit_test_view_model.do_set_tree, "succeed_delete_mission_phase"
        )
