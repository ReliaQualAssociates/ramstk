# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.pof.pof_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase
from ramstk.models.dbviews import RAMSTKPoFView


@pytest.mark.usefixtures("test_view_model")
class TestCreateModel:
    """Class for testing PoF view model initialization."""

    @pytest.mark.unit
    def test_view_model_create(self, test_view_model):
        """Should return a view model instance."""
        assert isinstance(test_view_model, RAMSTKPoFView)
        assert isinstance(test_view_model.tree, Tree)
        assert isinstance(test_view_model.dao, BaseDatabase)
        assert test_view_model._tag == "pof"
        assert test_view_model._root == 0
        assert test_view_model._revision_id == 0
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_opload")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_insert_opstress")
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_insert_test_method"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_mechanism"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_opload"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_opstress"
        )
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_retrieve_all_test_method"
        )
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_opload")
        assert pub.isSubscribed(test_view_model.do_set_tree, "succeed_delete_opstress")
        assert pub.isSubscribed(
            test_view_model.do_set_tree, "succeed_delete_test_method"
        )
