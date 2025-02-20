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
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectDesignElectric(SystemTestSelectMethods):
    """Class for testing Design Electric do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKDesignElectricRecord
    _select_id = 1
    _tag = "design_electric"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertDesignElectric(SystemTestInsertMethods):
    """Class for testing Design Electric table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should NOT add a record to the record tree."""
        assert integration_test_table_model.tree.get_node(9) is None

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

        assert integration_test_table_model.tree.get_node(9) is None

    @pytest.mark.integration
    def test_do_insert_sibling_part(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should add a record to the record tree."""
        assert integration_test_table_model.tree.get_node(10) is None

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
            integration_test_table_model.tree.get_node(10).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(10)
            .data["design_electric"]
            .revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(10)
            .data["design_electric"]
            .hardware_id
            == 10
        )

    @pytest.mark.skip(reason="Design Electric records are added by database.")
    def test_do_insert_sibling(self, test_attributes, integration_test_table_model):
        """Should not run because Design Electric are added by database."""
        pass

    @pytest.mark.skip(reason="Design Electric records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Design Electric is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Design Electric records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Design Electric is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Design Electric records are added by database.")
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should not run because Design Electric are added by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteDesignElectric(SystemTestDeleteMethods):
    """Class for testing Design Electric table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"

    @pytest.mark.skip(reason="Design Electric records are deleted by database.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Design Electric are deleted by database."""
        pass

    @pytest.mark.skip(reason="Design Electric records are deleted by database.")
    def test_do_delete_non_existent_id(self):
        """Should not run because Design Electric are deleted by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateDesignElectric:
    """Class for testing Design Electric update() and update_all() methods."""

    __test__ = True

    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_update_{self._tag} topic was broadcast.")

    def on_succeed_update_all(self):
        """Listen for succeed_update messages."""
        print(
            f"\033[36m\n\tsucceed_update_all topic was broadcast on update all "
            f"{self._tag}s"
        )

    def on_fail_update_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            f"The value for one or more attributes for "
            f"{self._tag.replace('_', ' ')} ID {self._update_id} was the wrong type."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on wrong data "
            f"type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent {self._tag.replace('_', ' ')} "
            f"with {self._tag.replace('_', ' ')} ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"No data package found for {self._tag.replace('_', ' ')} "
            f"ID {self._update_id}."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        _design_electric = integration_test_table_model.do_select(self._update_id)
        _design_electric.n_active_pins = 5
        _design_electric.temperature_active = 81
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        _design_electric = integration_test_table_model.do_select(self._update_id)
        _design_electric.n_active_pins = 5
        _design_electric.temperature_active = 81
        _design_electric = integration_test_table_model.do_select(self._update_id + 7)
        _design_electric.n_active_pins = 12
        _design_electric.temperature_active = 71

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .n_active_pins
            == 5
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .temperature_active
            == 81
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 7)
            .data[self._tag]
            .n_active_pins
            == 12
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 7)
            .data[self._tag]
            .temperature_active
            == 71
        )

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _design_electric = integration_test_table_model.do_select(self._update_id)
        _design_electric.temperature_active = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _design_electric = integration_test_table_model.do_select(self._update_id)
        _design_electric.temperature_active = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterDesignElectric(SystemTestGetterSetterMethods):
    """Class for testing Design Electric table getter and setter methods."""

    __test__ = True

    _package = {"temperature_active": 65.5}
    _record = RAMSTKDesignElectricRecord
    _tag = "design_electric"
    _test_id = 8


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDesignElectricAnalysisMethods:
    """Class for testing Design Electric analytical methods."""

    def on_fail_calculate_current_stress(self, logger_name, message):
        """Listen for fail_calculate messages."""
        assert logger_name == "DEBUG"
        assert message == (
            "Failed to calculate current ratio for hardware ID 1.  Rated current=0.0, "
            "operating current=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_current_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    def on_fail_calculate_power_stress(self, logger_name, message):
        """Listen for fail_calculate messages."""
        assert logger_name == "DEBUG"
        assert message == (
            "Failed to calculate power ratio for hardware ID 1.  Rated power=0.0, "
            "operating power=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_power_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    def on_fail_calculate_voltage_stress(self, logger_name, message):
        """Listen for fail_calculate messages."""
        assert logger_name == "DEBUG"
        assert message == (
            "Failed to calculate voltage ratio for hardware ID 1.  Rated voltage=0.0, "
            "operating ac voltage=0.0, operating DC voltage=0.0032."
        )
        print(
            "\033[35m\nfail_calculate_voltage_stress topic was broadcast on "
            "ZeroDivisionError."
        )

    @pytest.mark.integration
    def test_do_calculate_current_stress_zero_operating(
        self, integration_test_table_model
    ):
        """Should calculate the ratio of operating to rated current."""
        pub.subscribe(
            self.on_fail_calculate_current_stress,
            "do_log_debug_msg",
        )

        _design_electric = integration_test_table_model.do_select(1)
        _design_electric.current_rated = 0.0
        _design_electric.current_operating = 0.0032

        _design_electric.do_calculate_current_ratio()
        _attributes = integration_test_table_model.do_select(1).get_attributes()

        assert _attributes["current_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_current_stress,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_calculate_power_stress_zero_operating(
        self, integration_test_table_model
    ):
        """Should calculate the ratio of operating to rated power."""
        pub.subscribe(
            self.on_fail_calculate_power_stress,
            "do_log_debug_msg",
        )

        _design_electric = integration_test_table_model.do_select(1)
        _design_electric.power_rated = 0.0
        _design_electric.power_operating = 0.0032

        _design_electric.do_calculate_power_ratio()
        _attributes = integration_test_table_model.do_select(1).get_attributes()

        assert _attributes["power_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_power_stress,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_calculate_voltage_stress_zero_operating(
        self, integration_test_table_model
    ):
        """Should calculate the ratio of operating to rated voltage."""
        pub.subscribe(
            self.on_fail_calculate_voltage_stress,
            "do_log_debug_msg",
        )

        _design_electric = integration_test_table_model.do_select(1)
        _design_electric.voltage_rated = 0.0
        _design_electric.voltage_dc_operating = 0.0032

        _design_electric.do_calculate_voltage_ratio()
        _attributes = integration_test_table_model.do_select(1).get_attributes()

        assert _attributes["voltage_ratio"] == 0.0

        pub.unsubscribe(
            self.on_fail_calculate_voltage_stress,
            "do_log_debug_msg",
        )
