# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMechanism
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMechanism


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mechanism_1 = MockRAMSTKMechanism()
    _mechanism_1.revision_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 2
    _mechanism_1.description = "Test Failure Mechanism #1"
    _mechanism_1.rpn = 100
    _mechanism_1.rpn_new = 100
    _mechanism_1.rpn_detection = 10
    _mechanism_1.rpn_detection_new = 10
    _mechanism_1.rpn_occurrence_new = 10
    _mechanism_1.rpn_occurrence = 10
    _mechanism_1.pof_include = 1

    _mechanism_2 = MockRAMSTKMechanism()
    _mechanism_2.revision_id = 1
    _mechanism_2.mode_id = 1
    _mechanism_2.mechanism_id = 3
    _mechanism_2.description = "Test Failure Mechanism #2"
    _mechanism_2.rpn = 100
    _mechanism_2.rpn_new = 100
    _mechanism_2.rpn_detection = 10
    _mechanism_2.rpn_detection_new = 10
    _mechanism_2.rpn_occurrence_new = 10
    _mechanism_2.rpn_occurrence = 10
    _mechanism_2.pof_include = 1

    DAO = MockDAO()
    DAO.table = [
        _mechanism_1,
        _mechanism_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMechanism()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_mode")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut._do_insert_mechanism, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmMechanism)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "mechanisms"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_mode")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_mechanism_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_mechanism_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_mechanism"
        )
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_mechanism")
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_mode")
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_mechanism_tree"
        )
        assert pub.isSubscribed(test_datamanager._do_delete, "request_delete_mechanism")
        assert pub.isSubscribed(
            test_datamanager._do_insert_mechanism, "request_insert_mechanism"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMechanism instances on success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 1}
        )

        assert isinstance(
            test_datamanager.tree.get_node(2).data["mechanism"], MockRAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node(3).data["mechanism"], MockRAMSTKMechanism
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKMechanism on
        success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )

        _mechanism = test_datamanager.do_select(2, table="mechanism")

        assert isinstance(_mechanism, MockRAMSTKMechanism)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 10

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent mechanism ID is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )

        assert test_datamanager.do_select(100, table="mechanism") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_datamanager._do_insert_mechanism()

        assert test_datamanager.last_id == 4
        assert isinstance(
            test_datamanager.tree.get_node(4).data["mechanism"], RAMSTKMechanism
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_datamanager._do_delete(2)

        assert test_datamanager.last_id == 3
        assert test_datamanager.tree.get_node(2) is None
