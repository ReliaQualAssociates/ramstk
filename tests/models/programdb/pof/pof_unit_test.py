# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.pof.pof_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.models import RAMSTKPoFView


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKPoFView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_insert, "succeed_insert_mechanism")
    pub.unsubscribe(dut.on_insert, "succeed_insert_opload")
    pub.unsubscribe(dut.on_insert, "succeed_insert_opstress")
    pub.unsubscribe(dut.on_insert, "succeed_insert_test_method")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_oploads")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_opstresss")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_test_methods")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opload")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_opstress")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_test_method")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_viewmodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_viewmodel):
        """should return a view manager instance."""
        assert isinstance(test_viewmodel, RAMSTKPoFView)
        assert isinstance(test_viewmodel.tree, Tree)
        assert isinstance(test_viewmodel.dao, BaseDatabase)
        assert test_viewmodel._tag == "pof"
        assert test_viewmodel._root == 0
        assert test_viewmodel._revision_id == 0
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_opload")
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_opstress")
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_test_method")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_oploads")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_opstresss"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_test_methods"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_opload")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_opstress")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_test_method"
        )
