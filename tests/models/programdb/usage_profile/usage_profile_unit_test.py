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


@pytest.mark.usefixtures("test_view_model")
class TestCreateModel:
    """Class for testing view model initialization."""

    @pytest.mark.unit
    def test_view_model(self, test_view_model):
        """Should return a view model instance."""
        assert isinstance(test_view_model, RAMSTKUsageProfileView)
        assert isinstance(test_view_model.tree, Tree)
        assert isinstance(test_view_model.dao, BaseDatabase)
        assert test_view_model._tag == "usage_profile"
        assert test_view_model._root == 0
        assert test_view_model._revision_id == 0
        assert test_view_model._dic_load_functions == {
            "mission": test_view_model._do_load_missions,
            "mission_phase": test_view_model._do_load_mission_phases,
            "environment": test_view_model._do_load_environments,
        }
        assert isinstance(test_view_model._dic_trees["mission"], Tree)
        assert isinstance(test_view_model._dic_trees["mission_phase"], Tree)
        assert isinstance(test_view_model._dic_trees["environment"], Tree)
        assert test_view_model._lst_modules == [
            "mission",
            "mission_phase",
            "environment",
        ]
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_insert_environment"
        )
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_mission")
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_insert_mission_phase"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_environment"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_mission"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree,
            "succeed_retrieve_all_mission_phase",
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_delete_environment"
        )
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_mission")
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_delete_mission_phase"
        )
