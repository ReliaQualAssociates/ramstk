# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.pof.pof_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPoF
from ramstk.db.base import BaseDatabase


@pytest.fixture(scope="function")
def test_datamanager():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmPoF()
    # dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_opload_tree, "succeed_retrieve_oploads")
    pub.unsubscribe(dut.do_set_opstress_tree, "succeed_retrieve_opstresss")
    pub.unsubscribe(dut.do_set_test_method_tree, "succeed_retrieve_test_methods")
    pub.unsubscribe(dut.do_set_mechanism_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_opload_tree, "succeed_delete_opload")
    pub.unsubscribe(dut.do_set_opstress_tree, "succeed_delete_opstress")
    pub.unsubscribe(dut.do_set_test_method_tree, "succeed_delete_test_method")
    pub.unsubscribe(dut._on_insert, "succeed_insert_mechanism")
    pub.unsubscribe(dut._on_insert, "succeed_insert_opload")
    pub.unsubscribe(dut._on_insert, "succeed_insert_opstress")
    pub.unsubscribe(dut._on_insert, "succeed_insert_test_method")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmPoF)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, BaseDatabase)
        assert test_datamanager._tag == "pof"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_set_mechanism_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_opload_tree, "succeed_retrieve_oploads"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_opstress_tree, "succeed_retrieve_opstresss"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_test_method_tree, "succeed_retrieve_test_methods"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_mechanism_tree, "succeed_delete_mechanism"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_opload_tree, "succeed_delete_opload"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_opstress_tree, "succeed_delete_opstress"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_test_method_tree, "succeed_delete_test_method"
        )
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_opload")
        assert pub.isSubscribed(test_datamanager._on_insert, "succeed_insert_opstress")
        assert pub.isSubscribed(
            test_datamanager._on_insert, "succeed_insert_test_method"
        )
