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
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateDesignElectricModels:
    """Class for unit testing Design Electric model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return a Design Electric record model instance."""
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
    def test_table_model_create(self, unit_test_table_model):
        """Return a Design Electric table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKDesignElectricTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_design_electric"
        assert unit_test_table_model._select_msg == "selected_revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._tag == "design_electric"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKDesignElectricRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_design_electric_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_design_electric_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_design_electric"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_design_electric"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_design_electric_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_design_electric"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_design_electric"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_design_electric"
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree, "succeed_delete_hardware"
        )
        assert pub.isSubscribed(
            unit_test_table_model._do_update_tree, "succeed_insert_hardware"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectDesignElectric(UnitTestSelectMethods):
    """Class for unit testing Design Electric table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertDesignElectric(UnitTestInsertMethods):
    """Class for unit testing Design Electric table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"

    @pytest.mark.skip(reason="Design Electric records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Design Electric records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteDesignElectric(UnitTestDeleteMethods):
    """Class for unit testing Design Electric table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterDesignElectric(UnitTestGetterSetterMethods):
    """Class for unit testing Design Electric table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]
    _test_attr = "type_id"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

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


@pytest.mark.usefixtures(
    "test_attributes",
    "unit_test_table_model",
    "test_toml_user_configuration",
    "test_stress_limits",
)
class TestDesignElectricAnalysisMethods:
    """Class for testing Design Electric module analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_current_stress(self, test_attributes, unit_test_table_model):
        """Should calculate the current stress ratio."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _design_electric = unit_test_table_model.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.current_rated = 0.5
        _design_electric.current_operating = 0.0032

        _design_electric.do_calculate_current_ratio()
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == pytest.approx(0.0064)

    @pytest.mark.unit
    def test_do_calculate_power_stress(self, test_attributes, unit_test_table_model):
        """Should calculate the power stress ratio."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _design_electric = unit_test_table_model.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.power_rated = 0.1
        _design_electric.power_operating = 0.00009

        _design_electric.do_calculate_power_ratio()
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == pytest.approx(0.0009)

    @pytest.mark.unit
    def test_do_calculate_voltage_ratio(self, test_attributes, unit_test_table_model):
        """Should calculate the power stress ratio."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _design_electric = unit_test_table_model.do_select(1)
        _design_electric.hardware_id = 1
        _design_electric.voltage_rated = 50
        _design_electric.voltage_ac_operating = 0.005
        _design_electric.voltage_dc_operating = 3.3

        _design_electric.do_calculate_voltage_ratio()
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)

    @pytest.mark.unit
    def test_do_derating_analysis(
        self,
        test_attributes,
        unit_test_table_model,
        test_toml_user_configuration,
        test_stress_limits,
    ):
        """Should determine if a component is overstressed and the reason."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _design_electric = unit_test_table_model.do_select(1)
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
    def test_do_stress_analysis(self, test_attributes, unit_test_table_model):
        """Should calculate appropriate stress ratios for the component category."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _design_electric = unit_test_table_model.do_select(1)
        _design_electric.current_rated = 0.5
        _design_electric.current_operating = 0.0032
        _design_electric.power_rated = 0.1
        _design_electric.power_operating = 0.00009
        _design_electric.voltage_rated = 50
        _design_electric.voltage_ac_operating = 0.005
        _design_electric.voltage_dc_operating = 3.3

        _design_electric.do_stress_analysis(3)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == pytest.approx(0.0009)

        _design_electric.do_stress_analysis(5)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == pytest.approx(0.0064)
        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)
