# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.fmea.fmea_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase
from ramstk.models.dbviews import RAMSTKFMEAView


@pytest.mark.usefixtures("test_view_model")
class TestCreateModel:
    """Class for testing FMEA model initialization."""

    @pytest.mark.unit
    def test_view_model_create(self, test_view_model):
        """Should return a view model instance."""
        assert isinstance(test_view_model, RAMSTKFMEAView)
        assert isinstance(test_view_model.tree, Tree)
        assert isinstance(test_view_model.dao, BaseDatabase)
        assert test_view_model._tag == "fmeca"
        assert test_view_model._root == 0
        assert test_view_model._revision_id == 0
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_mode")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_cause")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_control")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_action")
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_mode"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_mechanism"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_cause"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_control"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_action"
        )
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_mode")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_cause")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_control")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_action")
