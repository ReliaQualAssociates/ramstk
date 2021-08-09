# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMechanism
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism
from ramstk.models.programdb import RAMSTKMechanism


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
    }


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mechanism_1 = MockRAMSTKMechanism()
    _mechanism_1.revision_id = 1
    _mechanism_1.hardware_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 1
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
    _mechanism_2.hardware_id = 1
    _mechanism_2.mode_id = 6
    _mechanism_2.mechanism_id = 2
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
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_mechanism_rpn")

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
        assert test_datamanager._db_id_colname == "fld_mechanism_id"
        assert test_datamanager._db_tablename == "ramstk_mechanism"
        assert test_datamanager._tag == "mechanism"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
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
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_mechanism_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_mechanism")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_mechanism")
        assert pub.isSubscribed(
            test_datamanager.do_calculate_rpn, "request_calculate_mechanism_rpn"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with RAMSTKMechanism
        instances on success."""
        test_datamanager.do_select_all(test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["mechanism"], MockRAMSTKMechanism
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["mechanism"], MockRAMSTKMechanism
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return an instance of the RAMSTKMechanism on success."""
        test_datamanager.do_select_all(test_attributes)

        _mechanism = test_datamanager.do_select(1)

        assert isinstance(_mechanism, MockRAMSTKMechanism)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 10

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """do_select() should return None when a non-existent mechanism ID is
        requested."""
        test_datamanager.do_select_all(test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)

        assert test_datamanager.tree.get_node(3) is None

        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(3).data["mechanism"], RAMSTKMechanism
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)
        test_datamanager.do_delete(2)

        assert test_datamanager.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, test_datamanager):
        """should calculate the mechanism RPN."""
        test_datamanager.do_select_all(test_attributes)

        test_datamanager.tree.get_node(1).data["mechanism"].rpn_occurrence = 8
        test_datamanager.tree.get_node(1).data["mechanism"].rpn_detection = 3
        test_datamanager.tree.get_node(2).data["mechanism"].rpn_occurrence = 4
        test_datamanager.tree.get_node(2).data["mechanism"].rpn_detection = 5

        test_datamanager.do_calculate_rpn(8)

        assert test_datamanager.tree.get_node(1).data["mechanism"].rpn == 192
        assert test_datamanager.tree.get_node(2).data["mechanism"].rpn == 160
