# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.design_electric.design_electric_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Electric module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKDesignElectricTable
from ramstk.models.programdb import RAMSTKDesignElectric


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _design_electric_1 = RAMSTKDesignElectric()
    _design_electric_1.revision_id = 1
    _design_electric_1.hardware_id = 1
    _design_electric_1.application_id = 0
    _design_electric_1.area = 0.0
    _design_electric_1.capacitance = 0.0
    _design_electric_1.configuration_id = 0
    _design_electric_1.construction_id = 0
    _design_electric_1.contact_form_id = 0
    _design_electric_1.contact_gauge = 0
    _design_electric_1.contact_rating_id = 0
    _design_electric_1.current_operating = 0.0
    _design_electric_1.current_rated = 0.0
    _design_electric_1.current_ratio = 0.0
    _design_electric_1.environment_active_id = 0
    _design_electric_1.environment_dormant_id = 0
    _design_electric_1.family_id = 0
    _design_electric_1.feature_size = 0.0
    _design_electric_1.frequency_operating = 0.0
    _design_electric_1.insert_id = 0
    _design_electric_1.insulation_id = 0
    _design_electric_1.manufacturing_id = 0
    _design_electric_1.matching_id = 0
    _design_electric_1.n_active_pins = 0
    _design_electric_1.n_circuit_planes = 1
    _design_electric_1.n_cycles = 0
    _design_electric_1.n_elements = 0
    _design_electric_1.n_hand_soldered = 0
    _design_electric_1.n_wave_soldered = 0
    _design_electric_1.operating_life = 0.0
    _design_electric_1.overstress = 0
    _design_electric_1.package_id = 0
    _design_electric_1.power_operating = 0.0
    _design_electric_1.power_rated = 0.0
    _design_electric_1.power_ratio = 0.0
    _design_electric_1.reason = ""
    _design_electric_1.resistance = 0.0
    _design_electric_1.specification_id = 0
    _design_electric_1.technology_id = 0
    _design_electric_1.temperature_active = 35.0
    _design_electric_1.temperature_case = 0.0
    _design_electric_1.temperature_dormant = 25.0
    _design_electric_1.temperature_hot_spot = 0.0
    _design_electric_1.temperature_junction = 0.0
    _design_electric_1.temperature_knee = 25.0
    _design_electric_1.temperature_rated_max = 0.0
    _design_electric_1.temperature_rated_min = 0.0
    _design_electric_1.temperature_rise = 0.0
    _design_electric_1.theta_jc = 0.0
    _design_electric_1.type_id = 0
    _design_electric_1.voltage_ac_operating = 0.0
    _design_electric_1.voltage_dc_operating = 0.0
    _design_electric_1.voltage_esd = 0.0
    _design_electric_1.voltage_rated = 0.0
    _design_electric_1.voltage_ratio = 0.0
    _design_electric_1.weight = 0.0
    _design_electric_1.years_in_production = 1

    _design_electric_2 = RAMSTKDesignElectric()
    _design_electric_2.revision_id = 1
    _design_electric_2.hardware_id = 2
    _design_electric_2.application_id = 0
    _design_electric_2.area = 0.0
    _design_electric_2.capacitance = 0.0
    _design_electric_2.configuration_id = 0
    _design_electric_2.construction_id = 0
    _design_electric_2.contact_form_id = 0
    _design_electric_2.contact_gauge = 0
    _design_electric_2.contact_rating_id = 0
    _design_electric_2.current_operating = 0.0
    _design_electric_2.current_rated = 0.0
    _design_electric_2.current_ratio = 0.0
    _design_electric_2.environment_active_id = 0
    _design_electric_2.environment_dormant_id = 0
    _design_electric_2.family_id = 0
    _design_electric_2.feature_size = 0.0
    _design_electric_2.frequency_operating = 0.0
    _design_electric_2.insert_id = 0
    _design_electric_2.insulation_id = 0
    _design_electric_2.manufacturing_id = 0
    _design_electric_2.matching_id = 0
    _design_electric_2.n_active_pins = 0
    _design_electric_2.n_circuit_planes = 1
    _design_electric_2.n_cycles = 0
    _design_electric_2.n_elements = 0
    _design_electric_2.n_hand_soldered = 0
    _design_electric_2.n_wave_soldered = 0
    _design_electric_2.operating_life = 0.0
    _design_electric_2.overstress = 0
    _design_electric_2.package_id = 0
    _design_electric_2.power_operating = 0.0
    _design_electric_2.power_rated = 0.0
    _design_electric_2.power_ratio = 0.0
    _design_electric_2.reason = ""
    _design_electric_2.resistance = 0.0
    _design_electric_2.specification_id = 0
    _design_electric_2.technology_id = 0
    _design_electric_2.temperature_active = 35.0
    _design_electric_2.temperature_case = 0.0
    _design_electric_2.temperature_dormant = 25.0
    _design_electric_2.temperature_hot_spot = 0.0
    _design_electric_2.temperature_junction = 0.0
    _design_electric_2.temperature_knee = 25.0
    _design_electric_2.temperature_rated_max = 0.0
    _design_electric_2.temperature_rated_min = 0.0
    _design_electric_2.temperature_rise = 0.0
    _design_electric_2.theta_jc = 0.0
    _design_electric_2.type_id = 0
    _design_electric_2.voltage_ac_operating = 0.0
    _design_electric_2.voltage_dc_operating = 0.0
    _design_electric_2.voltage_esd = 0.0
    _design_electric_2.voltage_rated = 0.0
    _design_electric_2.voltage_ratio = 0.0
    _design_electric_2.weight = 0.0
    _design_electric_2.years_in_production = 1

    _design_electric_3 = RAMSTKDesignElectric()
    _design_electric_3.revision_id = 1
    _design_electric_3.hardware_id = 3
    _design_electric_3.application_id = 0
    _design_electric_3.area = 0.0
    _design_electric_3.capacitance = 0.0
    _design_electric_3.configuration_id = 0
    _design_electric_3.construction_id = 0
    _design_electric_3.contact_form_id = 0
    _design_electric_3.contact_gauge = 0
    _design_electric_3.contact_rating_id = 0
    _design_electric_3.current_operating = 0.0
    _design_electric_3.current_rated = 0.0
    _design_electric_3.current_ratio = 0.0
    _design_electric_3.environment_active_id = 0
    _design_electric_3.environment_dormant_id = 0
    _design_electric_3.family_id = 0
    _design_electric_3.feature_size = 0.0
    _design_electric_3.frequency_operating = 0.0
    _design_electric_3.insert_id = 0
    _design_electric_3.insulation_id = 0
    _design_electric_3.manufacturing_id = 0
    _design_electric_3.matching_id = 0
    _design_electric_3.n_active_pins = 0
    _design_electric_3.n_circuit_planes = 1
    _design_electric_3.n_cycles = 0
    _design_electric_3.n_elements = 0
    _design_electric_3.n_hand_soldered = 0
    _design_electric_3.n_wave_soldered = 0
    _design_electric_3.operating_life = 0.0
    _design_electric_3.overstress = 0
    _design_electric_3.package_id = 0
    _design_electric_3.power_operating = 0.0
    _design_electric_3.power_rated = 0.0
    _design_electric_3.power_ratio = 0.0
    _design_electric_3.reason = ""
    _design_electric_3.resistance = 0.0
    _design_electric_3.specification_id = 0
    _design_electric_3.technology_id = 0
    _design_electric_3.temperature_active = 35.0
    _design_electric_3.temperature_case = 0.0
    _design_electric_3.temperature_dormant = 25.0
    _design_electric_3.temperature_hot_spot = 0.0
    _design_electric_3.temperature_junction = 0.0
    _design_electric_3.temperature_knee = 25.0
    _design_electric_3.temperature_rated_max = 0.0
    _design_electric_3.temperature_rated_min = 0.0
    _design_electric_3.temperature_rise = 0.0
    _design_electric_3.theta_jc = 0.0
    _design_electric_3.type_id = 0
    _design_electric_3.voltage_ac_operating = 0.0
    _design_electric_3.voltage_dc_operating = 0.0
    _design_electric_3.voltage_esd = 0.0
    _design_electric_3.voltage_rated = 0.0
    _design_electric_3.voltage_ratio = 0.0
    _design_electric_3.weight = 0.0
    _design_electric_3.years_in_production = 1

    DAO = MockDAO()
    DAO.table = [
        _design_electric_1,
        _design_electric_2,
        _design_electric_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "application_id": 0,
        "area": 0.0,
        "capacitance": 0.0,
        "configuration_id": 0,
        "construction_id": 0,
        "contact_form_id": 0,
        "contact_gauge": 0,
        "contact_rating_id": 0,
        "current_operating": 0.0,
        "current_rated": 0.0,
        "current_ratio": 0.0,
        "environment_active_id": 0,
        "environment_dormant_id": 0,
        "family_id": 0,
        "feature_size": 0.0,
        "frequency_operating": 0.0,
        "insert_id": 0,
        "insulation_id": 0,
        "manufacturing_id": 0,
        "matching_id": 0,
        "n_active_pins": 0,
        "n_circuit_planes": 1,
        "n_cycles": 0,
        "n_elements": 0,
        "n_hand_soldered": 0,
        "n_wave_soldered": 0,
        "operating_life": 0.0,
        "overstress": 0,
        "package_id": 0,
        "power_operating": 0.0,
        "power_rated": 0.0,
        "power_ratio": 0.0,
        "reason": "",
        "resistance": 0.0,
        "specification_id": 0,
        "technology_id": 0,
        "temperature_active": 35.0,
        "temperature_case": 0.0,
        "temperature_dormant": 25.0,
        "temperature_hot_spot": 0.0,
        "temperature_junction": 0.0,
        "temperature_knee": 25.0,
        "temperature_rated_max": 0.0,
        "temperature_rated_min": 0.0,
        "temperature_rise": 0.0,
        "theta_jc": 0.0,
        "type_id": 0,
        "voltage_ac_operating": 0.0,
        "voltage_dc_operating": 0.0,
        "voltage_esd": 0.0,
        "voltage_rated": 0.0,
        "voltage_ratio": 0.0,
        "weight": 0.0,
        "years_in_production": 1,
    }


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKDesignElectricTable()
    dut.do_connect(mock_program_dao)

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

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
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
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKDesignElectric
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


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectric,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["design_electric"],
            RAMSTKDesignElectric,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["design_electric"],
            RAMSTKDesignElectric,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)

        assert isinstance(_design_electric, RAMSTKDesignElectric)
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

        assert isinstance(_new_record, RAMSTKDesignElectric)
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
            test_tablemodel.tree.get_node(4).data["design_electric"],
            RAMSTKDesignElectric,
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


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
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

        test_tablemodel.do_calculate_current_ratio(1)
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

        test_tablemodel.do_calculate_power_ratio(1)
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

        test_tablemodel.do_calculate_voltage_ratio(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)
