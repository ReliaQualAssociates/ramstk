# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.design_mechanic.design_mechanic_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Design Mechanic module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKDesignMechanicRecord
from ramstk.models.dbtables import RAMSTKDesignMechanicTable, RAMSTKHardwareTable


@pytest.fixture(scope="class")
def test_hardware_table(test_program_dao):
    """Create test hardware table."""
    dut = RAMSTKHardwareTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

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

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_table_model(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKDesignMechanicTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

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
    pub.unsubscribe(dut._on_insert_hardware, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["design_mechanic"], RAMSTKDesignMechanicRecord
        )
        print("\033[36m\n\tsucceed_retrieve_design_mechanic topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_table_model):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_design_mechanic")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_design_mechanic")


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(9).data["design_mechanic"], RAMSTKDesignMechanicRecord
        )
        assert tree.get_node(9).data["design_mechanic"].hardware_id == 9
        print("\033[36m\n\tsucceed_insert_design_mechanic topic was broadcast.")

    def on_fail_insert_no_hardware(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(11) is not present in table "
            '"ramstk_hardware".'
        )
        print(
            "\033[35m\n\tfail_insert_design_mechanic topic was broadcast on no "
            "hardware."
        )

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should not add a record to the record tree and update last_id."""
        assert test_table_model.tree.get_node(9) is None

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 9,
                "parent_id": 2,
                "record_id": 9,
                "part": 0,
            },
        )

        assert test_table_model.tree.get_node(9) is None

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should add a record to the record tree and update last_id."""
        assert test_table_model.tree.get_node(10) is None

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 10,
                "parent_id": 2,
                "record_id": 10,
                "part": 1,
            },
        )

        assert isinstance(
            test_table_model.tree.get_node(10).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert (
            test_table_model.tree.get_node(10).data["design_mechanic"].revision_id == 1
        )
        assert (
            test_table_model.tree.get_node(10).data["design_mechanic"].hardware_id == 10
        )

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_table_model):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "do_log_debug_msg")

        assert test_table_model.tree.get_node(11) is None

        test_attributes["hardware_id"] = 11
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 11
        pub.sendMessage("request_insert_design_mechanic", attributes=test_attributes)

        assert test_table_model.tree.get_node(11) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\n\tsucceed_delete_design_mechanic topic was broadcast.")

    def on_fail_delete_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("Attempted to delete non-existent Design Mechanic ID 300.")
        print(
            "\033[35m\n\tfail_delete_design_mechanic topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_delete_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        # Two debug messages will be sent by two different methods under this scenario.
        try:
            assert message == (
                "No data package for node ID 1 in module design_mechanic."
            )
        except AssertionError:
            assert message == ("Attempted to delete non-existent Design Mechanic ID 1.")
        print(
            "\033[35m\n\tfail_delete_design_mechanic topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_table_model):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_design_mechanic")

        _last_id = test_table_model.last_id
        pub.sendMessage("request_delete_design_mechanic", node_id=_last_id)

        assert test_table_model.last_id == 1
        assert test_table_model.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_design_mechanic")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_delete_design_mechanic", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "do_log_debug_msg")

        test_table_model.tree.get_node(1).data.pop("design_mechanic")
        pub.sendMessage("request_delete_design_mechanic", node_id=1)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["design_mechanic"].altitude_operating == 5
        assert tree.get_node(1).data["design_mechanic"].rpm_operating == 81
        print("\033[36m\n\tsucceed_update_design_mechanic topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for Design Mechanic.")

    def on_fail_update_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "The value for one or more attributes for design mechanic ID 1 was the "
            "wrong type."
        )
        print(
            "\033[35m\n\tfail_update_design_mechanic topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("Attempting to update the root node 0.")
        print(
            "\033[35m\n\tfail_update_design_mechanic topic was broadcast on root node."
        )

    def on_fail_update_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "Attempted to save non-existent design mechanic with design mechanic "
            "ID 100."
        )
        print(
            "\033[35m\n\tfail_update_design_mechanic topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("No data package found for design mechanic ID 1.")
        print(
            "\033[35m\n\tfail_update_design_mechanic topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_table_model):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_design_mechanic")

        _design_mechanic = test_table_model.do_select(1)
        _design_mechanic.altitude_operating = 5
        _design_mechanic.rpm_operating = 81
        pub.sendMessage("request_update_design_mechanic", node_id=1)

        assert (
            test_table_model.tree.get_node(1).data["design_mechanic"].altitude_operating
            == 5
        )
        assert (
            test_table_model.tree.get_node(1).data["design_mechanic"].rpm_operating
            == 81
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_design_mechanic")

    @pytest.mark.integration
    def test_do_update_all(self, test_table_model):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_design_mechanic")

        _design_mechanic = test_table_model.do_select(1)
        _design_mechanic.altitude_operating = 5
        _design_mechanic.rpm_operating = 81
        _design_mechanic = test_table_model.do_select(8)
        _design_mechanic.altitude_operating = 12
        _design_mechanic.rpm_operating = 71

        pub.sendMessage("request_update_all_design_mechanic")

        assert (
            test_table_model.tree.get_node(1).data["design_mechanic"].altitude_operating
            == 5
        )
        assert (
            test_table_model.tree.get_node(1).data["design_mechanic"].rpm_operating
            == 81
        )
        assert (
            test_table_model.tree.get_node(8).data["design_mechanic"].altitude_operating
            == 12
        )
        assert (
            test_table_model.tree.get_node(8).data["design_mechanic"].rpm_operating
            == 71
        )

        pub.unsubscribe(
            self.on_succeed_update_all, "succeed_update_all_design_mechanic"
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_table_model):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _design_mechanic = test_table_model.do_select(1)
        _design_mechanic.altitude_operating = {1: 2}
        pub.sendMessage("request_update_design_mechanic", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_table_model):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _design_mechanic = test_table_model.do_select(1)
        _design_mechanic.altitude_operating = {1: 2}
        pub.sendMessage("request_update_design_mechanic", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_update_design_mechanic", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        test_table_model.tree.get_node(1).data.pop("design_mechanic")
        pub.sendMessage("request_update_design_mechanic", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 1
        assert attributes["altitude_operating"] == 0.0
        assert attributes["application_id"] == 0
        assert attributes["balance_id"] == 0
        assert attributes["clearance"] == 0.0
        assert attributes["casing_id"] == 0
        assert attributes["contact_pressure"] == 0.0
        assert attributes["deflection"] == 0.0
        assert attributes["diameter_coil"] == 0.0
        assert attributes["diameter_inner"] == 0.0
        assert attributes["diameter_outer"] == 0.0
        assert attributes["diameter_wire"] == 0.0
        assert attributes["filter_size"] == 0.0
        assert attributes["flow_design"] == 0.0
        assert attributes["flow_operating"] == 0.0
        assert attributes["frequency_operating"] == 0.0
        assert attributes["friction"] == 0.0
        assert attributes["impact_id"] == 0
        assert attributes["leakage_allowable"] == 0.0
        assert attributes["length"] == 0.0
        assert attributes["length_compressed"] == 0.0
        assert attributes["length_relaxed"] == 0.0
        assert attributes["load_design"] == 0.0
        assert attributes["load_id"] == 0
        assert attributes["load_operating"] == 0.0
        assert attributes["lubrication_id"] == 0
        assert attributes["manufacturing_id"] == 0
        assert attributes["material_id"] == 0
        assert attributes["meyer_hardness"] == 0.0
        assert attributes["misalignment_angle"] == 0.0
        assert attributes["n_ten"] == 0
        assert attributes["n_cycles"] == 0
        assert attributes["n_elements"] == 0
        assert attributes["offset"] == 0.0
        assert attributes["particle_size"] == 0.0
        assert attributes["pressure_contact"] == 0.0
        assert attributes["pressure_delta"] == 0.0
        assert attributes["pressure_downstream"] == 0.0
        assert attributes["pressure_rated"] == 0.0
        assert attributes["pressure_upstream"] == 0.0
        assert attributes["rpm_design"] == 0.0
        assert attributes["rpm_operating"] == 0.0
        assert attributes["service_id"] == 0
        assert attributes["spring_index"] == 0.0
        assert attributes["surface_finish"] == 0.0
        assert attributes["technology_id"] == 0
        assert attributes["thickness"] == 0.0
        assert attributes["torque_id"] == 0
        assert attributes["type_id"] == 0
        assert attributes["viscosity_design"] == 0.0
        assert attributes["viscosity_dynamic"] == 0.0
        assert attributes["water_per_cent"] == 0.0
        assert attributes["width_minimum"] == 0.0

        print("\033[36m\n\tsucceed_get_design_mechanic_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["design_mechanic"], RAMSTKDesignMechanicRecord
        )
        print("\033[36m\n\tsucceed_get_design_mechanic_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["design_mechanic"].rpm_design == 65.5
        print("\033[36m\n\tsucceed_get_design_mechanic_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_table_model_attributes(self, test_table_model):
        """should return the table model attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_design_mechanic_attributes"
        )

        test_table_model.do_get_attributes(node_id=1)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_design_mechanic_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_design_mechanic_tree"
        )

        pub.sendMessage("request_get_design_mechanic_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_design_mechanic_tree"
        )

    @pytest.mark.integration
    def test_do_set_table_model_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(
            self.on_succeed_set_attributes, "succeed_get_design_mechanic_tree"
        )

        pub.sendMessage(
            "request_set_design_mechanic_attributes",
            node_id=1,
            package={"rpm_design": 65.5},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes, "succeed_get_design_mechanic_tree"
        )
