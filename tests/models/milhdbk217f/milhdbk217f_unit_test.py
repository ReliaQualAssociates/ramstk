# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.milhdbk217f.milhdbk217f_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing MIL-HDBK-217F module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMILHDBK217FTable
from ramstk.models.programdb import RAMSTKMilHdbkF


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_milhdbk217f")
    pub.unsubscribe(dut.do_update, "request_update_milhdbk217f")
    pub.unsubscribe(dut.do_get_tree, "request_get_milhdbk217f_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_milhdbk217f")
    pub.unsubscribe(dut.do_insert, "request_insert_milhdbk217f")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKMILHDBK217FTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_mil_hdbk_f"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "milhdbk217f"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKMilHdbkF
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_milhdbk217f_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_milhdbk217f_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_milhdbk217f"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_milhdbk217f"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_milhdbk217f_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_milhdbk217f")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_milhdbk217f")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_milhdbk217f")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["milhdbk217f"],
            RAMSTKMilHdbkF,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["milhdbk217f"],
            RAMSTKMilHdbkF,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["milhdbk217f"],
            RAMSTKMilHdbkF,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _milhdbk217f = test_tablemodel.do_select(1)

        assert isinstance(_milhdbk217f, RAMSTKMilHdbkF)
        assert _milhdbk217f.revision_id == 1
        assert _milhdbk217f.hardware_id == 1
        assert _milhdbk217f.lambdaBD == 0.0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKMilHdbkF)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["milhdbk217f"],
            RAMSTKMilHdbkF,
        )
        assert test_tablemodel.tree.get_node(4).data["milhdbk217f"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["milhdbk217f"].hardware_id == 4


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(node_id=_last_id)

        assert test_tablemodel.last_id == 2
        assert test_tablemodel.tree.get_node(_last_id) is None
