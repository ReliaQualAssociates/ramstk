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
from ramstk.models.dbrecords import RAMSTKDesignMechanicRecord
from ramstk.models.dbtables import RAMSTKDesignMechanicTable


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


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for testing model initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """__init__() should create an RAMSTKDesignMechanic model."""
        assert isinstance(test_recordmodel, RAMSTKDesignMechanicRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_design_mechanic"
        assert test_recordmodel.hardware_id == 1
        assert test_recordmodel.altitude_operating == 0.0
        assert test_recordmodel.application_id == 0
        assert test_recordmodel.balance_id == 0
        assert test_recordmodel.clearance == 0.0
        assert test_recordmodel.casing_id == 0
        assert test_recordmodel.contact_pressure == 0.0
        assert test_recordmodel.deflection == 0.0
        assert test_recordmodel.diameter_coil == 0.0
        assert test_recordmodel.diameter_inner == 0.0
        assert test_recordmodel.diameter_outer == 0.0
        assert test_recordmodel.diameter_wire == 0.0
        assert test_recordmodel.filter_size == 0.0
        assert test_recordmodel.flow_design == 0.0
        assert test_recordmodel.flow_operating == 0.0
        assert test_recordmodel.frequency_operating == 0.0
        assert test_recordmodel.friction == 0.0
        assert test_recordmodel.impact_id == 0
        assert test_recordmodel.leakage_allowable == 0.0
        assert test_recordmodel.length == 0.0
        assert test_recordmodel.length_compressed == 0.0
        assert test_recordmodel.length_relaxed == 0.0
        assert test_recordmodel.load_design == 0.0
        assert test_recordmodel.load_id == 0
        assert test_recordmodel.load_operating == 0.0
        assert test_recordmodel.lubrication_id == 0
        assert test_recordmodel.manufacturing_id == 0
        assert test_recordmodel.material_id == 0
        assert test_recordmodel.meyer_hardness == 0.0
        assert test_recordmodel.misalignment_angle == 0.0
        assert test_recordmodel.n_ten == 0
        assert test_recordmodel.n_cycles == 0
        assert test_recordmodel.n_elements == 0
        assert test_recordmodel.offset == 0.0
        assert test_recordmodel.particle_size == 0.0
        assert test_recordmodel.pressure_contact == 0.0
        assert test_recordmodel.pressure_delta == 0.0
        assert test_recordmodel.pressure_downstream == 0.0
        assert test_recordmodel.pressure_rated == 0.0
        assert test_recordmodel.pressure_upstream == 0.0
        assert test_recordmodel.rpm_design == 0.0
        assert test_recordmodel.rpm_operating == 0.0
        assert test_recordmodel.service_id == 0
        assert test_recordmodel.spring_index == 0.0
        assert test_recordmodel.surface_finish == 0.0
        assert test_recordmodel.technology_id == 0
        assert test_recordmodel.thickness == 0.0
        assert test_recordmodel.torque_id == 0
        assert test_recordmodel.type_id == 0
        assert test_recordmodel.viscosity_design == 0.0
        assert test_recordmodel.viscosity_dynamic == 0.0
        assert test_recordmodel.water_per_cent == 0.0
        assert test_recordmodel.width_minimum == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
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
            "parent_id",
            "record_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKDesignMechanicRecord
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
            test_tablemodel.do_update_all, "request_update_all_design_mechanics"
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
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_mechanic = test_tablemodel.do_select(1)

        assert isinstance(_design_mechanic, RAMSTKDesignMechanicRecord)
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

        assert isinstance(_new_record, RAMSTKDesignMechanicRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 4

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 4
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
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


@pytest.mark.usefixtures("test_attributes", "mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, mock_program_dao):
        """should return the record model attributes dict."""
        dut = mock_program_dao.do_select_all(RAMSTKDesignMechanicRecord)[0]

        _attributes = dut.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["pressure_upstream"] == 0.0
        assert _attributes["frequency_operating"] == 0.0
        assert _attributes["surface_finish"] == 0.0
        assert _attributes["friction"] == 0.0
        assert _attributes["length_compressed"] == 0.0
        assert _attributes["load_id"] == 0
        assert _attributes["n_cycles"] == 0
        assert _attributes["balance_id"] == 0
        assert _attributes["lubrication_id"] == 0
        assert _attributes["water_per_cent"] == 0.0
        assert _attributes["misalignment_angle"] == 0.0
        assert _attributes["type_id"] == 0
        assert _attributes["rpm_design"] == 0.0
        assert _attributes["pressure_downstream"] == 0.0
        assert _attributes["diameter_coil"] == 0.0
        assert _attributes["manufacturing_id"] == 0
        assert _attributes["pressure_contact"] == 0.0
        assert _attributes["meyer_hardness"] == 0.0
        assert _attributes["rpm_operating"] == 0.0
        assert _attributes["length_relaxed"] == 0.0
        assert _attributes["impact_id"] == 0
        assert _attributes["n_ten"] == 0
        assert _attributes["material_id"] == 0
        assert _attributes["technology_id"] == 0
        assert _attributes["service_id"] == 0
        assert _attributes["flow_design"] == 0.0
        assert _attributes["application_id"] == 0
        assert _attributes["diameter_wire"] == 0.0
        assert _attributes["deflection"] == 0.0
        assert _attributes["filter_size"] == 0.0
        assert _attributes["diameter_inner"] == 0.0
        assert _attributes["pressure_rated"] == 0.0
        assert _attributes["hardware_id"] == 1
        assert _attributes["altitude_operating"] == 0.0
        assert _attributes["thickness"] == 0.0
        assert _attributes["diameter_outer"] == 0.0
        assert _attributes["n_elements"] == 0
        assert _attributes["contact_pressure"] == 0.0
        assert _attributes["particle_size"] == 0.0
        assert _attributes["casing_id"] == 0
        assert _attributes["viscosity_dynamic"] == 0.0
        assert _attributes["viscosity_design"] == 0.0
        assert _attributes["torque_id"] == 0
        assert _attributes["leakage_allowable"] == 0.0
        assert _attributes["offset"] == 0.0
        assert _attributes["width_minimum"] == 0.0
        assert _attributes["load_operating"] == 0.0
        assert _attributes["spring_index"] == 0.0
        assert _attributes["flow_operating"] == 0.0
        assert _attributes["pressure_delta"] == 0.0
        assert _attributes["length"] == 0.0
        assert _attributes["load_design"] == 0.0
        assert _attributes["clearance"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, mock_program_dao):
        """should set the value of the attribute requested."""
        dut = mock_program_dao.do_select_all(RAMSTKDesignMechanicRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert dut.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, mock_program_dao
    ):
        """should set an attribute to it's default value when passed a None value."""
        dut = mock_program_dao.do_select_all(RAMSTKDesignMechanicRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes["type_id"] = None

        assert dut.set_attributes(test_attributes) is None
        assert dut.get_attributes()["type_id"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, mock_program_dao
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        dut = mock_program_dao.do_select_all(RAMSTKDesignMechanicRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            dut.set_attributes({"shibboly-bibbly-boo": 0.9998})
