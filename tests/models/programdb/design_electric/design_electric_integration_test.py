# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.design_electric.design_electric_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Electric module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKDesignElectricRecord
from ramstk.models.dbtables import RAMSTKDesignElectricTable, RAMSTKHardwareTable


@pytest.fixture(scope="class")
def test_table_model(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKDesignElectricTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

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


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["design_electric"], RAMSTKDesignElectricRecord
        )
        print("\033[36m\n\tsucceed_retrieve_design_electric topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_table_model):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(
            self.on_succeed_select_all, "succeed_retrieve_all_design_electric"
        )

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(
            self.on_succeed_select_all, "succeed_retrieve_all_design_electric"
        )


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should NOT add a record to the record tree."""
        assert test_table_model.tree.get_node(9) is None

        # The design electric record is added by the database whenever a hardware
        # record is added to the database.  Adding the new allocation record to the
        # Design Electric tree is triggered by the "succeed_insert_hardware" message.
        # Only records associated with part type hardware are added to the Design
        # Electric tree.
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 9,
                "parent_id": 2,
                "part": 0,
            },
        )

        assert test_table_model.tree.get_node(9) is None

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should add a record to the record tree."""
        assert test_table_model.tree.get_node(10) is None

        # The design electric record is added by the database whenever a hardware
        # record is added to the database.  Adding the new allocation record to the
        # Design Electric tree is triggered by the "succeed_insert_hardware" message.
        # Only records associated with part type hardware are added to the Design
        # Electric tree.
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 10,
                "parent_id": 2,
                "part": 1,
            },
        )

        assert isinstance(
            test_table_model.tree.get_node(10).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert (
            test_table_model.tree.get_node(10).data["design_electric"].revision_id == 1
        )
        assert (
            test_table_model.tree.get_node(10).data["design_electric"].hardware_id == 10
        )


@pytest.mark.usefixtures("test_table_model", "test_hardware_table")
class TestDeleteMethods:
    """Class for testing the do_delete() method."""

    def on_succeed_delete_hardware(self, tree):
        assert tree.get_node(8) is None
        print("\033[36m\n\tsucceed_delete_hardware topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_table_model, test_hardware_table):
        """should remove record from record tree."""
        pub.subscribe(self.on_succeed_delete_hardware, "succeed_delete_hardware")

        assert isinstance(
            test_table_model.tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )

        # Allocation records are cascade deleted by the database server whenever the
        # corresponding Hardware record is deleted.
        pub.sendMessage("request_delete_hardware", node_id=8)

        assert test_table_model.tree.get_node(8) is None

        pub.unsubscribe(self.on_succeed_delete_hardware, "succeed_delete_hardware")


@pytest.mark.usefixtures("test_table_model")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["design_electric"].parent_id == 1
        assert tree.get_node(2).data["design_electric"].n_active_pins == 5
        assert tree.get_node(2).data["design_electric"].temperature_active == 81
        print("\033[36m\n\tsucceed_update_design_electric topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for design electric.")

    def on_fail_update_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "The value for one or more attributes for design electric ID 1 was the "
            "wrong type."
        )
        print(
            "\033[35m\n\tfail_update_design_electric topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("Attempting to update the root node 0.")
        print(
            "\033[35m\n\tfail_update_design_electric topic was broadcast on root node."
        )

    def on_fail_update_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "Attempted to save non-existent design electric with design electric "
            "ID 100."
        )
        print(
            "\033[35m\n\tfail_update_design_electric topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("No data package found for design electric ID 1.")
        print(
            "\033[35m\n\tfail_update_design_electric topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_table_model):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_design_electric")

        _design_electric = test_table_model.do_select(8)
        _design_electric.n_active_pins = 5
        _design_electric.temperature_active = 81
        pub.sendMessage("request_update_design_electric", node_id=8)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_design_electric")

    @pytest.mark.integration
    def test_do_update_all(self, test_table_model):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_design_electric")

        _design_electric = test_table_model.do_select(1)
        _design_electric.n_active_pins = 5
        _design_electric.temperature_active = 81
        _design_electric = test_table_model.do_select(8)
        _design_electric.n_active_pins = 12
        _design_electric.temperature_active = 71

        pub.sendMessage("request_update_all_design_electric")

        assert (
            test_table_model.tree.get_node(1).data["design_electric"].n_active_pins == 5
        )
        assert (
            test_table_model.tree.get_node(1).data["design_electric"].temperature_active
            == 81
        )
        assert (
            test_table_model.tree.get_node(8).data["design_electric"].n_active_pins
            == 12
        )
        assert (
            test_table_model.tree.get_node(8).data["design_electric"].temperature_active
            == 71
        )

        pub.unsubscribe(
            self.on_succeed_update_all, "succeed_update_all_design_electric"
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_table_model):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _design_electric = test_table_model.do_select(1)
        _design_electric.temperature_active = {1: 2}
        pub.sendMessage("request_update_design_electric", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_table_model):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _design_electric = test_table_model.do_select(1)
        _design_electric.temperature_active = {1: 2}
        pub.sendMessage("request_update_design_electric", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_update_design_electric", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        test_table_model.tree.get_node(1).data.pop("design_electric")
        pub.sendMessage("request_update_design_electric", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 8
        assert attributes["application_id"] == 0
        assert attributes["area"] == 0.0
        assert attributes["capacitance"] == 0.0
        assert attributes["configuration_id"] == 0
        assert attributes["construction_id"] == 0
        assert attributes["contact_form_id"] == 0
        assert attributes["contact_gauge"] == 0
        assert attributes["contact_rating_id"] == 0
        assert attributes["current_operating"] == 0.0
        assert attributes["current_rated"] == 0.0
        assert attributes["current_ratio"] == 0.0
        assert attributes["environment_active_id"] == 0
        assert attributes["environment_dormant_id"] == 0
        assert attributes["family_id"] == 0
        assert attributes["feature_size"] == 0.0
        assert attributes["frequency_operating"] == 0.0
        assert attributes["insert_id"] == 0
        assert attributes["insulation_id"] == 0
        assert attributes["manufacturing_id"] == 0
        assert attributes["matching_id"] == 0
        assert attributes["n_active_pins"] == 0
        assert attributes["n_circuit_planes"] == 1
        assert attributes["n_cycles"] == 0
        assert attributes["n_elements"] == 0
        assert attributes["n_hand_soldered"] == 0
        assert attributes["n_wave_soldered"] == 0
        assert attributes["operating_life"] == 0.0
        assert attributes["overstress"] == 0
        assert attributes["package_id"] == 0
        assert attributes["power_operating"] == 0.0
        assert attributes["power_rated"] == 0.0
        assert attributes["power_ratio"] == 0.0
        assert attributes["reason"] == ""
        assert attributes["resistance"] == 0.0
        assert attributes["specification_id"] == 0
        assert attributes["technology_id"] == 0
        assert attributes["temperature_active"] == 35.0
        assert attributes["temperature_case"] == 0.0
        assert attributes["temperature_dormant"] == 25.0
        assert attributes["temperature_hot_spot"] == 0.0
        assert attributes["temperature_junction"] == 0.0
        assert attributes["temperature_knee"] == 25.0
        assert attributes["temperature_rated_max"] == 0.0
        assert attributes["temperature_rated_min"] == 0.0
        assert attributes["temperature_rise"] == 0.0
        assert attributes["theta_jc"] == 0.0
        assert attributes["type_id"] == 0
        assert attributes["voltage_ac_operating"] == 0.0
        assert attributes["voltage_dc_operating"] == 0.0
        assert attributes["voltage_esd"] == 0.0
        assert attributes["voltage_rated"] == 0.0
        assert attributes["voltage_ratio"] == 0.0
        assert attributes["weight"] == 0.0
        assert attributes["years_in_production"] == 1

        print("\033[36m\n\tsucceed_get_design_electric_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["design_electric"], RAMSTKDesignElectricRecord
        )
        print("\033[36m\n\tsucceed_get_design_electric_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(8).data["design_electric"].temperature_active == 65.5
        print("\033[36m\n\tsucceed_get_design_electric_tree topic was broadcast.")

    @pytest.mark.integration
    def test_do_get_table_model_attributes(self, test_table_model):
        """should return the table model attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_design_electric_attributes"
        )

        test_table_model.do_get_attributes(node_id=8)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_design_electric_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_design_electric_tree"
        )

        pub.sendMessage("request_get_design_electric_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_design_electric_tree"
        )

    @pytest.mark.integration
    def test_do_set_table_model_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(
            self.on_succeed_set_attributes, "succeed_get_design_electric_tree"
        )

        pub.sendMessage(
            "request_set_design_electric_attributes",
            node_id=8,
            package={"temperature_active": 65.5},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes, "succeed_get_design_electric_tree"
        )


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_fail_calculate_current_stress(self, error_message):
        assert error_message == (
            "Failed to calculate current ratio for hardware ID 1.  Rated current=0.0, "
            "operating current=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_current_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    def on_fail_calculate_power_stress(self, error_message):
        assert error_message == (
            "Failed to calculate power ratio for hardware ID 1.  Rated power=0.0, "
            "operating power=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_power_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    def on_fail_calculate_voltage_stress(self, error_message):
        assert error_message == (
            "Failed to calculate voltage ratio for hardware ID 1.  Rated voltage=0.0, "
            "operating ac voltage=0.0, operating DC voltage=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_voltage_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    @pytest.mark.integration
    def test_do_calculate_current_stress_zero_operating(self, test_table_model):
        """should calculate the ratio of operating to rated current."""
        pub.subscribe(
            self.on_fail_calculate_current_stress,
            "fail_calculate_current_stress",
        )

        _design_electric = test_table_model.do_select(1)
        _design_electric.current_rated = 0.0
        _design_electric.current_operating = 0.0032

        _design_electric.do_calculate_current_ratio()
        _attributes = test_table_model.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_current_stress,
            "fail_calculate_current_stress",
        )

    @pytest.mark.integration
    def test_do_calculate_power_stress_zero_operating(self, test_table_model):
        """should calculate the ratio of operating to rated power."""
        pub.subscribe(
            self.on_fail_calculate_power_stress,
            "fail_calculate_power_stress",
        )

        _design_electric = test_table_model.do_select(1)
        _design_electric.power_rated = 0.0
        _design_electric.power_operating = 0.0032

        _design_electric.do_calculate_power_ratio()
        _attributes = test_table_model.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_power_stress,
            "fail_calculate_power_stress",
        )

    @pytest.mark.integration
    def test_do_calculate_voltage_stress_zero_operating(self, test_table_model):
        """should calculate the ratio of operating to rated voltage."""
        pub.subscribe(
            self.on_fail_calculate_voltage_stress,
            "fail_calculate_voltage_stress",
        )

        _design_electric = test_table_model.do_select(1)
        _design_electric.voltage_rated = 0.0
        _design_electric.voltage_dc_operating = 0.0032

        _design_electric.do_calculate_voltage_ratio()
        _attributes = test_table_model.do_select(1).get_attributes()

        assert _attributes["voltage_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_voltage_stress,
            "fail_calculate_voltage_stress",
        )
