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
    pub.unsubscribe(dut.do_derating_analysis, "request_derating_analysis")
    pub.unsubscribe(dut.do_stress_analysis, "request_stress_analysis")

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
        assert test_tablemodel._dic_stress_limits == {}
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


@pytest.mark.usefixtures(
    "test_attributes", "test_tablemodel", "test_toml_user_configuration"
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

    @pytest.mark.unit
    def test_do_derating_analysis_over_limit(
        self, test_attributes, test_tablemodel, test_toml_user_configuration
    ):
        """should determine if a component is overstressed and the reason."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        test_tablemodel._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )
        _design_electric.hardware_id = 1
        _design_electric.current_ratio = 1.62
        _design_electric.power_ratio = 0.55
        _design_electric.voltage_ratio = 0.58

        test_tablemodel.do_derating_analysis(1, 3)
        assert _design_electric.overstress
        assert (
            _design_electric.reason
            == "Operating current is greater than limit in a harsh "
            "environment.\nOperating current is greater than limit in a mild "
            "environment.\nOperating power is greater than limit in a harsh "
            "environment.\n"
        )

        test_tablemodel.do_derating_analysis(1, 5)
        assert _design_electric.overstress
        assert (
            _design_electric.reason
            == "Operating current is greater than limit in a harsh environment.\n"
            "Operating current is greater than limit in a mild environment.\n"
            "Operating voltage is greater than limit in a harsh environment.\n"
        )

    @pytest.mark.unit
    def test_do_derating_analysis_under_limit(
        self, test_attributes, test_tablemodel, test_toml_user_configuration
    ):
        """should determine if a component is overstressed and the reason."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _design_electric = test_tablemodel.do_select(1)
        test_tablemodel._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )
        _design_electric.hardware_id = 1
        _design_electric.current_ratio = -0.62
        _design_electric.power_ratio = -0.55
        _design_electric.voltage_ratio = -0.58

        test_tablemodel.do_derating_analysis(1, 3)
        assert _design_electric.overstress
        assert (
            _design_electric.reason
            == "Operating current is less than limit in a harsh "
            "environment.\nOperating current is less than limit in a mild "
            "environment.\nOperating power is less than limit in a harsh "
            "environment.\nOperating power is less than limit in a mild "
            "environment.\nOperating voltage is less than limit in a harsh "
            "environment.\nOperating voltage is less than limit in a mild "
            "environment.\n"
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

        test_tablemodel.do_stress_analysis(1, 3)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == pytest.approx(0.0009)

        test_tablemodel.do_stress_analysis(1, 5)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == pytest.approx(0.0064)
        assert _attributes["voltage_ratio"] == pytest.approx(0.0661)
