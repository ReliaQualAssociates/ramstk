# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.design_mechanic.design_mechanic_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Mechanic module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKDesignMechanicTable
from ramstk.models.programdb import RAMSTKDesignMechanic


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _design_mechanic_1 = RAMSTKDesignMechanic()
    _design_mechanic_1.revision_id = 1
    _design_mechanic_1.hardware_id = 1
    _design_mechanic_1.altitude_operating = 0.0
    _design_mechanic_1.application_id = 0
    _design_mechanic_1.balance_id = 0
    _design_mechanic_1.clearance = 0.0
    _design_mechanic_1.casing_id = 0
    _design_mechanic_1.contact_pressure = 0.0
    _design_mechanic_1.deflection = 0.0
    _design_mechanic_1.diameter_coil = 0.0
    _design_mechanic_1.diameter_inner = 0.0
    _design_mechanic_1.diameter_outer = 0.0
    _design_mechanic_1.diameter_wire = 0.0
    _design_mechanic_1.filter_size = 0.0
    _design_mechanic_1.flow_design = 0.0
    _design_mechanic_1.flow_operating = 0.0
    _design_mechanic_1.frequency_operating = 0.0
    _design_mechanic_1.friction = 0.0
    _design_mechanic_1.impact_id = 0
    _design_mechanic_1.leakage_allowable = 0.0
    _design_mechanic_1.length = 0.0
    _design_mechanic_1.length_compressed = 0.0
    _design_mechanic_1.length_relaxed = 0.0
    _design_mechanic_1.load_design = 0.0
    _design_mechanic_1.load_id = 0
    _design_mechanic_1.load_operating = 0.0
    _design_mechanic_1.lubrication_id = 0
    _design_mechanic_1.manufacturing_id = 0
    _design_mechanic_1.material_id = 0
    _design_mechanic_1.meyer_hardness = 0.0
    _design_mechanic_1.misalignment_angle = 0.0
    _design_mechanic_1.n_ten = 0
    _design_mechanic_1.n_cycles = 0
    _design_mechanic_1.n_elements = 0
    _design_mechanic_1.offset = 0.0
    _design_mechanic_1.particle_size = 0.0
    _design_mechanic_1.pressure_contact = 0.0
    _design_mechanic_1.pressure_delta = 0.0
    _design_mechanic_1.pressure_downstream = 0.0
    _design_mechanic_1.pressure_rated = 0.0
    _design_mechanic_1.pressure_upstream = 0.0
    _design_mechanic_1.rpm_design = 0.0
    _design_mechanic_1.rpm_operating = 0.0
    _design_mechanic_1.service_id = 0
    _design_mechanic_1.spring_index = 0.0
    _design_mechanic_1.surface_finish = 0.0
    _design_mechanic_1.technology_id = 0
    _design_mechanic_1.thickness = 0.0
    _design_mechanic_1.torque_id = 0
    _design_mechanic_1.type_id = 0
    _design_mechanic_1.viscosity_design = 0.0
    _design_mechanic_1.viscosity_dynamic = 0.0
    _design_mechanic_1.water_per_cent = 0.0
    _design_mechanic_1.width_minimum = 0.0

    _design_mechanic_2 = RAMSTKDesignMechanic()
    _design_mechanic_2.revision_id = 1
    _design_mechanic_2.hardware_id = 2
    _design_mechanic_2.altitude_operating = 0.0
    _design_mechanic_2.application_id = 0
    _design_mechanic_2.balance_id = 0
    _design_mechanic_2.clearance = 0.0
    _design_mechanic_2.casing_id = 0
    _design_mechanic_2.contact_pressure = 0.0
    _design_mechanic_2.deflection = 0.0
    _design_mechanic_2.diameter_coil = 0.0
    _design_mechanic_2.diameter_inner = 0.0
    _design_mechanic_2.diameter_outer = 0.0
    _design_mechanic_2.diameter_wire = 0.0
    _design_mechanic_2.filter_size = 0.0
    _design_mechanic_2.flow_design = 0.0
    _design_mechanic_2.flow_operating = 0.0
    _design_mechanic_2.frequency_operating = 0.0
    _design_mechanic_2.friction = 0.0
    _design_mechanic_2.impact_id = 0
    _design_mechanic_2.leakage_allowable = 0.0
    _design_mechanic_2.length = 0.0
    _design_mechanic_2.length_compressed = 0.0
    _design_mechanic_2.length_relaxed = 0.0
    _design_mechanic_2.load_design = 0.0
    _design_mechanic_2.load_id = 0
    _design_mechanic_2.load_operating = 0.0
    _design_mechanic_2.lubrication_id = 0
    _design_mechanic_2.manufacturing_id = 0
    _design_mechanic_2.material_id = 0
    _design_mechanic_2.meyer_hardness = 0.0
    _design_mechanic_2.misalignment_angle = 0.0
    _design_mechanic_2.n_ten = 0
    _design_mechanic_2.n_cycles = 0
    _design_mechanic_2.n_elements = 0
    _design_mechanic_2.offset = 0.0
    _design_mechanic_2.particle_size = 0.0
    _design_mechanic_2.pressure_contact = 0.0
    _design_mechanic_2.pressure_delta = 0.0
    _design_mechanic_2.pressure_downstream = 0.0
    _design_mechanic_2.pressure_rated = 0.0
    _design_mechanic_2.pressure_upstream = 0.0
    _design_mechanic_2.rpm_design = 0.0
    _design_mechanic_2.rpm_operating = 0.0
    _design_mechanic_2.service_id = 0
    _design_mechanic_2.spring_index = 0.0
    _design_mechanic_2.surface_finish = 0.0
    _design_mechanic_2.technology_id = 0
    _design_mechanic_2.thickness = 0.0
    _design_mechanic_2.torque_id = 0
    _design_mechanic_2.type_id = 0
    _design_mechanic_2.viscosity_design = 0.0
    _design_mechanic_2.viscosity_dynamic = 0.0
    _design_mechanic_2.water_per_cent = 0.0
    _design_mechanic_2.width_minimum = 0.0

    _design_mechanic_3 = RAMSTKDesignMechanic()
    _design_mechanic_3.revision_id = 1
    _design_mechanic_3.hardware_id = 3
    _design_mechanic_3.altitude_operating = 0.0
    _design_mechanic_3.application_id = 0
    _design_mechanic_3.balance_id = 0
    _design_mechanic_3.clearance = 0.0
    _design_mechanic_3.casing_id = 0
    _design_mechanic_3.contact_pressure = 0.0
    _design_mechanic_3.deflection = 0.0
    _design_mechanic_3.diameter_coil = 0.0
    _design_mechanic_3.diameter_inner = 0.0
    _design_mechanic_3.diameter_outer = 0.0
    _design_mechanic_3.diameter_wire = 0.0
    _design_mechanic_3.filter_size = 0.0
    _design_mechanic_3.flow_design = 0.0
    _design_mechanic_3.flow_operating = 0.0
    _design_mechanic_3.frequency_operating = 0.0
    _design_mechanic_3.friction = 0.0
    _design_mechanic_3.impact_id = 0
    _design_mechanic_3.leakage_allowable = 0.0
    _design_mechanic_3.length = 0.0
    _design_mechanic_3.length_compressed = 0.0
    _design_mechanic_3.length_relaxed = 0.0
    _design_mechanic_3.load_design = 0.0
    _design_mechanic_3.load_id = 0
    _design_mechanic_3.load_operating = 0.0
    _design_mechanic_3.lubrication_id = 0
    _design_mechanic_3.manufacturing_id = 0
    _design_mechanic_3.material_id = 0
    _design_mechanic_3.meyer_hardness = 0.0
    _design_mechanic_3.misalignment_angle = 0.0
    _design_mechanic_3.n_ten = 0
    _design_mechanic_3.n_cycles = 0
    _design_mechanic_3.n_elements = 0
    _design_mechanic_3.offset = 0.0
    _design_mechanic_3.particle_size = 0.0
    _design_mechanic_3.pressure_contact = 0.0
    _design_mechanic_3.pressure_delta = 0.0
    _design_mechanic_3.pressure_downstream = 0.0
    _design_mechanic_3.pressure_rated = 0.0
    _design_mechanic_3.pressure_upstream = 0.0
    _design_mechanic_3.rpm_design = 0.0
    _design_mechanic_3.rpm_operating = 0.0
    _design_mechanic_3.service_id = 0
    _design_mechanic_3.spring_index = 0.0
    _design_mechanic_3.surface_finish = 0.0
    _design_mechanic_3.technology_id = 0
    _design_mechanic_3.thickness = 0.0
    _design_mechanic_3.torque_id = 0
    _design_mechanic_3.type_id = 0
    _design_mechanic_3.viscosity_design = 0.0
    _design_mechanic_3.viscosity_dynamic = 0.0
    _design_mechanic_3.water_per_cent = 0.0
    _design_mechanic_3.width_minimum = 0.0

    DAO = MockDAO()
    DAO.table = [
        _design_mechanic_1,
        _design_mechanic_2,
        _design_mechanic_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "altitude_operating": 0.0,
        "application_id": 0,
        "balance_id": 0,
        "clearance": 0.0,
        "casing_id": 0,
        "contact_pressure": 0.0,
        "deflection": 0.0,
        "diameter_coil": 0.0,
        "diameter_inner": 0.0,
        "diameter_outer": 0.0,
        "diameter_wire": 0.0,
        "filter_size": 0.0,
        "flow_design": 0.0,
        "flow_operating": 0.0,
        "frequency_operating": 0.0,
        "friction": 0.0,
        "impact_id": 0,
        "leakage_allowable": 0.0,
        "length": 0.0,
        "length_compressed": 0.0,
        "length_relaxed": 0.0,
        "load_design": 0.0,
        "load_id": 0,
        "load_operating": 0.0,
        "lubrication_id": 0,
        "manufacturing_id": 0,
        "material_id": 0,
        "meyer_hardness": 0.0,
        "misalignment_angle": 0.0,
        "n_ten": 0,
        "n_cycles": 0,
        "n_elements": 0,
        "offset": 0.0,
        "particle_size": 0.0,
        "pressure_contact": 0.0,
        "pressure_delta": 0.0,
        "pressure_downstream": 0.0,
        "pressure_rated": 0.0,
        "pressure_upstream": 0.0,
        "rpm_design": 0.0,
        "rpm_operating": 0.0,
        "service_id": 0,
        "spring_index": 0.0,
        "surface_finish": 0.0,
        "technology_id": 0,
        "thickness": 0.0,
        "torque_id": 0,
        "type_id": 0,
        "viscosity_design": 0.0,
        "viscosity_dynamic": 0.0,
        "water_per_cent": 0.0,
        "width_minimum": 0.0,
    }


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKDesignMechanicTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_design_mechanic_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_design_mechanic_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_design_mechanic")
    pub.unsubscribe(dut.do_update, "request_update_design_mechanic")
    pub.unsubscribe(dut.do_get_tree, "request_get_design_mechanic_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_design_mechanic")
    pub.unsubscribe(dut.do_insert, "request_insert_design_mechanic")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKDesignMechanicTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_design_mechanic"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "design_mechanic"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKDesignMechanic
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_design_mechanic_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_design_mechanic_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_design_mechanic"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_design_mechanic"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_design_mechanic_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update, "request_update_design_mechanic"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_delete, "request_delete_design_mechanic"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_insert, "request_insert_design_mechanic"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["design_mechanic"],
            RAMSTKDesignMechanic,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["design_mechanic"],
            RAMSTKDesignMechanic,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["design_mechanic"],
            RAMSTKDesignMechanic,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_mechanic = test_tablemodel.do_select(1)

        assert isinstance(_design_mechanic, RAMSTKDesignMechanic)
        assert _design_mechanic.revision_id == 1
        assert _design_mechanic.hardware_id == 1
        assert _design_mechanic.rpm_design == 0.0

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

        assert isinstance(_new_record, RAMSTKDesignMechanic)
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
            test_tablemodel.tree.get_node(4).data["design_mechanic"],
            RAMSTKDesignMechanic,
        )
        assert test_tablemodel.tree.get_node(4).data["design_mechanic"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["design_mechanic"].hardware_id == 4


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
