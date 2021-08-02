# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.control.control_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Control algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKControl
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmControl
from ramstk.models.programdb import RAMSTKControl


@pytest.fixture
def mock_program_dao(monkeypatch):
    _control_1 = MockRAMSTKControl()
    _control_1.revision_id = 1
    _control_1.hardware_id = 1
    _control_1.mode_id = 6
    _control_1.mechanism_id = 3
    _control_1.cause_id = 3
    _control_1.control_id = 1
    _control_1.description = "Test FMEA Control #1 for Cause ID #3."
    _control_1.type_id = "Detection"

    _control_2 = MockRAMSTKControl()
    _control_2.revision_id = 1
    _control_2.hardware_id = 1
    _control_2.mode_id = 6
    _control_2.mechanism_id = 3
    _control_2.cause_id = 3
    _control_2.control_id = 2
    _control_2.description = "Test FMEA Control #2 for Cause ID #3."
    _control_2.type_id = "Prevention"

    DAO = MockDAO()
    DAO.table = [
        _control_1,
        _control_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "control_id": 3,
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmControl()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_control_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_control")
    pub.unsubscribe(dut.do_update, "request_update_control")
    pub.unsubscribe(dut.do_select_all, "selected_cause")
    pub.unsubscribe(dut.do_get_tree, "request_get_control_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_control")
    pub.unsubscribe(dut.do_insert, "request_insert_control")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmControl)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_control_id"
        assert test_datamanager._db_tablename == "ramstk_control"
        assert test_datamanager._tag == "control"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_cause")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_control_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_control_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_control"
        )
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_control")
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_control_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_control")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_control")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a Tree() object populated with RAMSTKControl instances."""
        test_datamanager.do_select_all(test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["control"], MockRAMSTKControl
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["control"], MockRAMSTKControl
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return an instance of the RAMSTKControl on success."""
        test_datamanager.do_select_all(test_attributes)

        _control = test_datamanager.do_select(1, table="control")

        assert isinstance(_control, MockRAMSTKControl)
        assert _control.description == "Test FMEA Control #1 for Cause ID #3."
        assert _control.type_id == "Detection"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """should return None when a non-existent control ID is requested."""
        test_datamanager.do_select_all(test_attributes)

        assert test_datamanager.do_select(100, table="control") is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree.get_node(3).data["control"], RAMSTKControl
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)
        test_datamanager.do_delete(2)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(2) is None
