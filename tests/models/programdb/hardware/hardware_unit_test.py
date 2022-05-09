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
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase
from ramstk.models.dbrecords import RAMSTKHardwareRecord
from ramstk.models.dbtables import RAMSTKHardwareTable
from ramstk.models.dbviews import RAMSTKHardwareBoMView
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a table model instance for each test function."""
    # Create the device under test (dut).
    dut = RAMSTKHardwareBoMView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_reliability")
    pub.unsubscribe(dut.do_calculate_hardware, "request_calculate_hardware")
    pub.unsubscribe(dut.do_make_composite_ref_des, "request_make_comp_ref_des")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateHardwareModels:
    """Class for unit testing Hardware model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Hardware record model instance."""
        pass

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Hardware table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKHardwareTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_hardware"
        assert unit_test_table_model._select_msg == "selected_revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._tag == "hardware"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
            "parent_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKHardwareRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_hardware_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_hardware_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_hardware_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_hardware"
        )

    @pytest.mark.unit
    def test_view_model_create(self, test_viewmodel):
        """Return a Hardware BoM view model instance."""
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
        assert test_viewmodel._dic_stress_limits == {
            "integrated_circuit": {},
            "semiconductor": {},
            "resistor": {},
            "capacitor": {},
            "inductor": {},
            "relay": {},
            "switch": {},
            "connection": {},
            "miscellaneous": {},
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
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_hardware")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_design_electric"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_design_mechanic"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_milhdbk217f"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_nswc")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_insert_reliability"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_all_hardware"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_all_design_electric"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_all_design_mechanic"
        )
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_all_milhdbk217f"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_all_nswc")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_all_reliability"
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
        assert pub.isSubscribed(
            test_viewmodel.do_make_composite_ref_des, "request_make_comp_ref_des"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectHardware(UnitTestSelectMethods):
    """Class for unit testing Hardware table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKHardwareRecord
    _tag = "hardware"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertHardware(UnitTestInsertMethods):
    """Class for unit testing Hardware table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKHardwareRecord
    _tag = "hardware"

    @pytest.mark.unit
    def test_do_make_comp_ref_des(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should create the composite reference designator."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(1)
        _hardware.ref_des = "SS8"

        _hardware = unit_test_table_model.do_select(2)
        _hardware.ref_des = "A9"

        test_viewmodel.do_make_composite_ref_des(1)

        assert unit_test_table_model.do_select(1).comp_ref_des == "SS8"
        assert unit_test_table_model.do_select(2).comp_ref_des == "SS8:A9"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteHardware(UnitTestDeleteMethods):
    """Class for unit testing Hardware table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKHardwareRecord
    _tag = "hardware"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterHardware(UnitTestGetterSetterMethods):
    """Class for unit testing Hardware table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "parent_id",
    ]

    _test_attr = "nsn"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["alt_part_number"] == ""
        assert _attributes["attachments"] == ""
        assert _attributes["cage_code"] == ""
        assert _attributes["category_id"] == 0
        assert _attributes["comp_ref_des"] == "S1"
        assert _attributes["cost"] == 0.0
        assert _attributes["cost_failure"] == 0.0
        assert _attributes["cost_hour"] == 0.0
        assert _attributes["cost_type_id"] == 2
        assert _attributes["description"] == "Test System"
        assert _attributes["duty_cycle"] == 100.0
        assert _attributes["figure_number"] == ""
        assert _attributes["lcn"] == ""
        assert _attributes["level"] == 0
        assert _attributes["manufacturer_id"] == 0
        assert _attributes["mission_time"] == 100.0
        assert _attributes["name"] == ""
        assert _attributes["nsn"] == ""
        assert _attributes["page_number"] == ""
        assert _attributes["parent_id"] == 0
        assert _attributes["part"] == 0
        assert _attributes["part_number"] == ""
        assert _attributes["quantity"] == 1
        assert _attributes["ref_des"] == "S1"
        assert _attributes["remarks"] == ""
        assert _attributes["repairable"] == 0
        assert _attributes["specification_number"] == ""
        assert _attributes["subcategory_id"] == 0
        assert _attributes["tagged_part"] == 0
        assert _attributes["total_cost"] == 0.0
        assert _attributes["total_part_count"] == 0
        assert _attributes["total_power_dissipation"] == 0.0
        assert _attributes["year_of_manufacture"] == 2019


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model", "test_viewmodel")
class TestHardwareAnalysisMethods:
    """Class for testing Hardware analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_cost_part(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should calculate the total cost for a part."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(3)
        _hardware.cost_type_id = 2
        _hardware.part = 1
        _hardware.cost = 12.98
        _hardware.quantity = 2

        test_viewmodel.do_calculate_cost(3)
        _attributes = unit_test_table_model.do_select(3).get_attributes()

        assert _attributes["total_cost"] == 25.96

    @pytest.mark.unit
    def test_do_calculate_cost_assembly(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should calculate the total cost of an assembly."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(1)
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = unit_test_table_model.do_select(2)
        _hardware.cost_type_id = 2
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = unit_test_table_model.do_select(3)
        _hardware.cost_type_id = 1
        _hardware.part = 1
        _hardware.cost = 12.98

        test_viewmodel.do_calculate_cost(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["total_cost"] == 38.94

    @pytest.mark.unit
    def test_do_calculate_cost_no_type_id(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should calculate the total cost for a part."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(3)
        _hardware.cost_type_id = 0
        _hardware.part = 1
        _hardware.cost = 12.98
        _hardware.quantity = 2

        test_viewmodel.do_calculate_cost(3)
        _attributes = unit_test_table_model.do_select(3).get_attributes()

        assert _attributes["total_cost"] == 0.0

    @pytest.mark.unit
    def test_do_calculate_part_count_part(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should calculate the total part count of a part."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(3)
        _hardware.part = 1
        _hardware.quantity = 2

        test_viewmodel.do_calculate_part_count(3)
        _attributes = unit_test_table_model.do_select(3).get_attributes()

        assert _attributes["total_part_count"] == 2

    @pytest.mark.unit
    def test_do_calculate_part_count_assembly(
        self, test_attributes, unit_test_table_model, test_viewmodel
    ):
        """Should calculate the total part count of an assembly."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _hardware = unit_test_table_model.do_select(1)
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = unit_test_table_model.do_select(2)
        _hardware.part = 0
        _hardware.quantity = 3
        _hardware = unit_test_table_model.do_select(3)
        _hardware.part = 1
        _hardware.quantity = 2

        test_viewmodel.do_calculate_part_count(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["total_part_count"] == 6
