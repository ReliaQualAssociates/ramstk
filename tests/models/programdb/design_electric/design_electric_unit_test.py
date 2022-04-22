# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.design_electric.design_electric_unit_test.py is part of
#       The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Electric module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKDesignElectricRecord
from ramstk.models.dbtables import RAMSTKDesignElectricTable

# noinspection PyUnresolvedReferences
from tests import MockDAO


@pytest.fixture(scope="function")
def test_tablemodel(mock_dao):
    """Get a data model instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKDesignElectricTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_design_electric_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_design_electric_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_design_electric")
    pub.unsubscribe(dut.do_update, "request_update_design_electric")
    pub.unsubscribe(dut.do_get_tree, "request_get_design_electric_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_design_electric")
    pub.unsubscribe(dut.do_insert, "request_insert_design_electric")
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "test_tablemodel")
class TestCreateModels:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKDesignElectricRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_design_electric"
        assert test_record_model.hardware_id == 1
        assert test_record_model.application_id == 0
        assert test_record_model.area == 0.0
        assert test_record_model.capacitance == 0.0
        assert test_record_model.configuration_id == 0
        assert test_record_model.construction_id == 0
        assert test_record_model.contact_form_id == 0
        assert test_record_model.contact_gauge == 0
        assert test_record_model.contact_rating_id == 0
        assert test_record_model.current_operating == 0.0
        assert test_record_model.current_rated == 0.0
        assert test_record_model.current_ratio == 0.0
        assert test_record_model.environment_active_id == 0
        assert test_record_model.environment_dormant_id == 0
        assert test_record_model.family_id == 0
        assert test_record_model.feature_size == 0.0
        assert test_record_model.frequency_operating == 0.0
        assert test_record_model.insert_id == 0
        assert test_record_model.insulation_id == 0
        assert test_record_model.manufacturing_id == 0
        assert test_record_model.matching_id == 0
        assert test_record_model.n_active_pins == 0
        assert test_record_model.n_circuit_planes == 1
        assert test_record_model.n_cycles == 0
        assert test_record_model.n_elements == 0
        assert test_record_model.n_hand_soldered == 0
        assert test_record_model.n_wave_soldered == 0
        assert test_record_model.operating_life == 0.0
        assert test_record_model.overstress == 0
        assert test_record_model.package_id == 0
        assert test_record_model.power_operating == 0.0
        assert test_record_model.power_rated == 0.0
        assert test_record_model.power_ratio == 0.0
        assert test_record_model.reason == ""
        assert test_record_model.resistance == 0.0
        assert test_record_model.specification_id == 0
        assert test_record_model.technology_id == 0
        assert test_record_model.temperature_active == 35.0
        assert test_record_model.temperature_case == 0.0
        assert test_record_model.temperature_dormant == 25.0
        assert test_record_model.temperature_hot_spot == 0.0
        assert test_record_model.temperature_junction == 0.0
        assert test_record_model.temperature_rated_max == 0.0
        assert test_record_model.temperature_rated_min == 0.0
        assert test_record_model.temperature_rise == 0.0
        assert test_record_model.theta_jc == 0.0
        assert test_record_model.type_id == 0
        assert test_record_model.voltage_ac_operating == 0.0
        assert test_record_model.voltage_dc_operating == 0.0
        assert test_record_model.voltage_esd == 0.0
        assert test_record_model.voltage_rated == 0.0
        assert test_record_model.voltage_ratio == 0.0
        assert test_record_model.weight == 0.0
        assert test_record_model.years_in_production == 1

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKDesignElectricTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_design_electric"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "design_electric"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
            "parent_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKDesignElectricRecord
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_design_electric_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_design_electric_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_design_electric"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_design_electric"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_design_electric_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update, "request_update_design_electric"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_delete, "request_delete_design_electric"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_insert, "request_insert_design_electric"
        )
        assert pub.isSubscribed(
            test_tablemodel._do_update_tree, "succeed_delete_hardware"
        )
        assert pub.isSubscribed(
            test_tablemodel._do_update_tree, "succeed_insert_hardware"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)

        assert isinstance(_design_electric, RAMSTKDesignElectricRecord)
        assert _design_electric.revision_id == 1
        assert _design_electric.hardware_id == 1
        assert _design_electric.environment_active_id == 0

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

        assert isinstance(_new_record, RAMSTKDesignElectricRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_attributes["parent_id"] = 1
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert test_tablemodel.tree.get_node(4).data["design_electric"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["design_electric"].hardware_id == 4


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


@pytest.mark.usefixtures("test_tablemodel", "test_toml_user_configuration")
class TestGetterSetterMethods:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, mock_dao):
        """should return the record model attributes dict."""
        dut = mock_dao.do_select_all(RAMSTKDesignElectricRecord)[0]

        _attributes = dut.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["voltage_ac_operating"] == 0.0
        assert _attributes["frequency_operating"] == 0.0
        assert _attributes["type_id"] == 0
        assert _attributes["resistance"] == 0.0
        assert _attributes["package_id"] == 0
        assert _attributes["technology_id"] == 0
        assert _attributes["n_cycles"] == 0
        assert _attributes["n_circuit_planes"] == 1
        assert _attributes["contact_gauge"] == 0
        assert _attributes["current_operating"] == 0.0
        assert _attributes["n_hand_soldered"] == 0
        assert _attributes["contact_rating_id"] == 0
        assert _attributes["area"] == 0.0
        assert _attributes["contact_form_id"] == 0
        assert _attributes["years_in_production"] == 1
        assert _attributes["n_active_pins"] == 0
        assert _attributes["capacitance"] == 0.0
        assert _attributes["temperature_case"] == 0.0
        assert _attributes["current_rated"] == 0.0
        assert _attributes["power_operating"] == 0.0
        assert _attributes["configuration_id"] == 0
        assert _attributes["temperature_hot_spot"] == 0.0
        assert _attributes["temperature_junction"] == 0.0
        assert _attributes["current_ratio"] == 0.0
        assert _attributes["insulation_id"] == 0
        assert _attributes["construction_id"] == 0
        assert _attributes["insert_id"] == 0
        assert _attributes["theta_jc"] == 0.0
        assert _attributes["voltage_dc_operating"] == 0.0
        assert _attributes["power_ratio"] == 0.0
        assert _attributes["family_id"] == 0
        assert _attributes["overstress"] == 0
        assert _attributes["voltage_rated"] == 0.0
        assert _attributes["feature_size"] == 0.0
        assert _attributes["operating_life"] == 0.0
        assert _attributes["application_id"] == 0
        assert _attributes["weight"] == 0.0
        assert _attributes["temperature_rated_max"] == 0.0
        assert _attributes["voltage_ratio"] == 0.0
        assert _attributes["temperature_rated_min"] == 0.0
        assert _attributes["power_rated"] == 0.0
        assert _attributes["environment_active_id"] == 0
        assert _attributes["hardware_id"] == 1
        assert _attributes["specification_id"] == 0
        assert _attributes["matching_id"] == 0
        assert _attributes["n_elements"] == 0
        assert _attributes["environment_dormant_id"] == 0
        assert _attributes["reason"] == ""
        assert _attributes["voltage_esd"] == 0.0
        assert _attributes["manufacturing_id"] == 0
        assert _attributes["n_wave_soldered"] == 0
        assert _attributes["temperature_knee"] == 25.0
        assert _attributes["temperature_rise"] == 0.0
        assert _attributes["temperature_active"] == 35.0
        assert _attributes["temperature_dormant"] == 25.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, mock_dao):
        """should set the value of the attribute requested."""
        dut = mock_dao.do_select_all(RAMSTKDesignElectricRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert dut.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(self, test_attributes, mock_dao):
        """should set an attribute to it's default value when passed a None value."""
        dut = mock_dao.do_select_all(RAMSTKDesignElectricRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes["type_id"] = None

        assert dut.set_attributes(test_attributes) is None
        assert dut.get_attributes()["type_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, mock_dao
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        dut = mock_dao.do_select_all(RAMSTKDesignElectricRecord)[0]

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            dut.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures(
    "test_attributes",
    "test_tablemodel",
    "test_toml_user_configuration",
    "test_stress_limits",
)
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_current_stress(self, test_attributes, test_tablemodel):
        """should calculate the current stress ratio."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.current_rated = 0.5
        _design_electric.current_operating = 0.0032

        _design_electric.do_calculate_current_ratio()
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == pytest.approx(0.0064)

    @pytest.mark.unit
    def test_do_calculate_power_stress(self, test_attributes, test_tablemodel):
        """should calculate the power stress ratio."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.power_rated = 0.1
        _design_electric.power_operating = 0.00009

        _design_electric.do_calculate_power_ratio()
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == pytest.approx(0.0009)

    @pytest.mark.unit
    def test_do_calculate_voltage_ratio(self, test_attributes, test_tablemodel):
        """should calculate the power stress ratio."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.voltage_rated = 50
        _design_electric.voltage_ac_operating = 0.005
        _design_electric.voltage_dc_operating = 3.3

        _design_electric.do_calculate_voltage_ratio()
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)

    @pytest.mark.unit
    def test_do_derating_analysis(
        self,
        test_attributes,
        test_tablemodel,
        test_toml_user_configuration,
        test_stress_limits,
    ):
        """should determine if a component is overstressed and the reason."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.environment_active_id = 2
        _design_electric.specification_id = 1
        _design_electric.temperature_case = 78.2
        _design_electric.temperature_rated_max = 85.0
        _design_electric.voltage_ratio = 0.58

        _design_electric.do_derating_analysis(
            4,
            10,
            2,
            test_stress_limits,
        )
        assert _design_electric.overstress == 1
        assert (
            _design_electric.reason == "Case temperature of 78.2C exceeds the derated "
            "maximum temperature of 15.0C less than maximum rated temperature of "
            "85.0C.\n"
        )

    @pytest.mark.unit
    def test_do_stress_analysis(self, test_attributes, test_tablemodel):
        """should calculate appropriate stress ratios for the component category."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        _design_electric.current_rated = 0.5
        _design_electric.current_operating = 0.0032
        _design_electric.power_rated = 0.1
        _design_electric.power_operating = 0.00009
        _design_electric.voltage_rated = 50
        _design_electric.voltage_ac_operating = 0.005
        _design_electric.voltage_dc_operating = 3.3

        _design_electric.do_stress_analysis(3)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == pytest.approx(0.0009)

        _design_electric.do_stress_analysis(5)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == pytest.approx(0.0064)
        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)
