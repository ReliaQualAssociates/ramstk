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
from ramstk.db.base import BaseDatabase
from ramstk.models import RAMSTKHardwareBoMView, RAMSTKHardwareTable
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


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareBoMView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_insert, "succeed_insert_hardware")
    pub.unsubscribe(dut.on_insert, "succeed_insert_design_electric")
    pub.unsubscribe(dut.on_insert, "succeed_insert_design_mechanic")
    pub.unsubscribe(dut.on_insert, "succeed_insert_milhdbk217f")
    pub.unsubscribe(dut.on_insert, "succeed_insert_nswc")
    pub.unsubscribe(dut.on_insert, "succeed_insert_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_hardwares")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_design_electrics")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_design_mechanics")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_milhdbk217fs")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_nswcs")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_reliabilitys")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_reliability")
    pub.unsubscribe(
        dut.do_calculate_power_dissipation, "request_calculate_power_dissipation"
    )
    pub.unsubscribe(
        dut.do_predict_active_hazard_rate, "request_predict_active_hazard_rate"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel", "test_viewmodel")
class TestCreateModels:
    """Class for testing model initialization."""

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
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

    @pytest.mark.unit
    def test_view_model_create(self, test_viewmodel):
        """should return a view manager instance."""
        assert isinstance(test_viewmodel, RAMSTKHardwareBoMView)
        assert isinstance(test_viewmodel.tree, Tree)
        assert isinstance(test_viewmodel.dao, BaseDatabase)
        assert test_viewmodel._tag == "hardware_bom"
        assert test_viewmodel._root == 0
        assert test_viewmodel._revision_id == 0
        assert test_viewmodel._dic_load_functions == {
            "hardware": test_viewmodel._do_load_hardware,
            "design_electric": test_viewmodel._do_load_design_electric,
            "design_mechanic": test_viewmodel._do_load_design_mechanic,
            "milhdbk217f": test_viewmodel._do_load_milhdbk217f,
            "nswc": test_viewmodel._do_load_nswc,
            "reliability": test_viewmodel._do_load_reliability,
        }
        assert isinstance(test_viewmodel._dic_trees["hardware"], Tree)
        assert isinstance(test_viewmodel._dic_trees["design_electric"], Tree)
        assert isinstance(test_viewmodel._dic_trees["design_mechanic"], Tree)
        assert isinstance(test_viewmodel._dic_trees["milhdbk217f"], Tree)
        assert isinstance(test_viewmodel._dic_trees["nswc"], Tree)
        assert isinstance(test_viewmodel._dic_trees["reliability"], Tree)
        assert test_viewmodel._lst_modules == [
            "hardware",
            "design_electric",
            "design_mechanic",
            "milhdbk217f",
            "nswc",
            "reliability",
        ]
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_hardware")
        assert pub.isSubscribed(
            test_viewmodel.on_insert, "succeed_insert_design_electric"
        )
        assert pub.isSubscribed(
            test_viewmodel.on_insert, "succeed_insert_design_mechanic"
        )
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_milhdbk217f")
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_nswc")
        assert pub.isSubscribed(test_viewmodel.on_insert, "succeed_insert_reliability")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_hardwares"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_design_electrics"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_design_mechanics"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_milhdbk217fs"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_nswcs")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_reliabilitys"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_hardware")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_design_electric"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_design_mechanic"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_milhdbk217f"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_nswc")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_delete_reliability"
        )


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

    @pytest.mark.unit
    def test_do_make_comp_ref_des(self, test_attributes, test_tablemodel):
        """should create the composite reference designator."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hardware = test_tablemodel.do_select(1)
        _hardware.ref_des = "SS8"

        _hardware = test_tablemodel.do_select(2)
        _hardware.ref_des = "A9"

        test_tablemodel.do_make_composite_ref_des(1)

        assert test_tablemodel.do_select(1).comp_ref_des == "SS8"
        assert test_tablemodel.do_select(2).comp_ref_des == "SS8:A9"


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
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(2)
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = test_tablemodel.do_select(3)
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
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(2)
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = test_tablemodel.do_select(3)
        _hardware.part = 1
        _hardware.quantity = 2

        test_tablemodel.do_calculate_part_count(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["total_part_count"] == 6
