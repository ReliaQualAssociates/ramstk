# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.hardware.hardware_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKHardwareTable
from ramstk.models.programdb import RAMSTKHardware


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hardware_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_hardware")
    pub.unsubscribe(dut.do_update, "request_update_hardware")
    pub.unsubscribe(dut.do_get_tree, "request_get_hardware_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_hardware")
    pub.unsubscribe(dut.do_insert, "request_insert_hardware")
    pub.unsubscribe(dut.do_calculate_cost, "request_calculate_total_cost")
    pub.unsubscribe(dut.do_calculate_part_count, "request_calculate_total_part_count")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKHardwareTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_hardware"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "hardware"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKHardware
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_hardware_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_hardware_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_hardware"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_hardware"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_hardware_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_hardware")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_hardware")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_hardware")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["hardware"],
            RAMSTKHardware,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["hardware"],
            RAMSTKHardware,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["hardware"],
            RAMSTKHardware,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(1)

        assert isinstance(_hardware, RAMSTKHardware)
        assert _hardware.revision_id == 1
        assert _hardware.hardware_id == 1
        assert _hardware.year_of_manufacture == 2019

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

        assert isinstance(_new_record, RAMSTKHardware)
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
            test_tablemodel.tree.get_node(4).data["hardware"],
            RAMSTKHardware,
        )
        assert test_tablemodel.tree.get_node(4).data["hardware"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["hardware"].hardware_id == 4


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


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_cost_part(self, test_attributes, test_tablemodel):
        """should calculate the total cost for a part."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(3)
        _hardware.hardware_id = 1
        _hardware.cost_type_id = 2
        _hardware.part = 1
        _hardware.cost = 12.98
        _hardware.quantity = 2

        test_tablemodel.do_calculate_cost(3)
        _attributes = test_tablemodel.do_select(3).get_attributes()

        assert _attributes["total_cost"] == 25.96

    @pytest.mark.unit
    def test_do_calculate_cost_assembly(self, test_attributes, test_tablemodel):
        """should calculate the total cost of an assembly."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(1)
        _hardware.hardware_id = 1
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(2)
        _hardware.hardware_id = 2
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = test_tablemodel.do_select(3)
        _hardware.hardware_id = 3
        _hardware.cost_type_id = 1
        _hardware.part = 1
        _hardware.total_cost = 25.96

        test_tablemodel.do_calculate_cost(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["total_cost"] == 77.88

    @pytest.mark.unit
    def test_do_calculate_part_count_part(self, test_attributes, test_tablemodel):
        """should calculate the total part count of a part."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(3)
        _hardware.hardware_id = 1
        _hardware.part = 1
        _hardware.quantity = 2

        test_tablemodel.do_calculate_part_count(3)
        _attributes = test_tablemodel.do_select(3).get_attributes()

        assert _attributes["total_part_count"] == 2

    @pytest.mark.unit
    def test_do_calculate_part_count_assembly(self, test_attributes, test_tablemodel):
        """should calculate the total part count of an assembly."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(1)
        _hardware.hardware_id = 1
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(2)
        _hardware.hardware_id = 2
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = test_tablemodel.do_select(3)
        _hardware.hardware_id = 3
        _hardware.part = 1
        _hardware.quantity = 2

        test_tablemodel.do_calculate_part_count(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["total_part_count"] == 6
