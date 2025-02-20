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
class TestSelectDesignMechanic(SystemTestSelectMethods):
    """Class for testing Design Mechanic do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKDesignMechanicRecord
    _select_id = 1
    _tag = "design_mechanic"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertDesignMechanic(SystemTestInsertMethods):
    """Class for testing Design Mechanic table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should NOT add a record to the record tree."""
        assert integration_test_table_model.tree.get_node(9) is None

        # The design mechanic record is added by the database whenever a hardware
        # record is added to the database.  Adding the new allocation record to the
        # Design Mechanic tree is triggered by the "succeed_insert_hardware" message.
        # Only records associated with part type hardware are added to the Design
        # Mechanic tree.
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
    def test_do_insert_part(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should add a record to the record tree and update last_id."""
        assert integration_test_table_model.tree.get_node(10) is None

        # The design mechanic record is added by the database whenever a hardware
        # record is added to the database.  Adding the new allocation record to the
        # Design Mechanic tree is triggered by the "succeed_insert_hardware" message.
        # Only records associated with part type hardware are added to the Design
        # Mechanic tree.
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
            integration_test_table_model.tree.get_node(10).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(10)
            .data["design_mechanic"]
            .revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(10)
            .data["design_mechanic"]
            .hardware_id
            == 10
        )

    @pytest.mark.skip(reason="Design Mechanic records are added by database.")
    def test_do_insert_sibling(self, test_attributes, integration_test_table_model):
        """Should not run because Design Mechanic are added by database."""
        pass

    @pytest.mark.skip(reason="Design Mechanic records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Design Mechanic is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Design Mechanic records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Design Mechanic is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Design Mechanic records are added by database.")
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should not run because Design Mechanic are added by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteDesignMechanic(SystemTestDeleteMethods):
    """Class for testing Design Mechanic table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"

    @pytest.mark.skip(reason="Design Mechanic records are deleted by database.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Design Mechanic are deleted by database."""
        pass

    @pytest.mark.skip(reason="Design Mechanic records are deleted by database.")
    def test_do_delete_non_existent_id(self):
        """Should not run because Design Mechanic are deleted by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateMethodsDesignMechanic:
    """Class for testing Design Mechanic update() and update_all() methods."""

    __test__ = True

    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_update_{self._update_id} topic was broadcast.")

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

        _design_mechanic = integration_test_table_model.do_select(self._update_id)
        _design_mechanic.altitude_operating = 5
        _design_mechanic.rpm_operating = 81
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .altitude_operating
            == 5
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .rpm_operating
            == 81
        )

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        _design_mechanic = integration_test_table_model.do_select(self._update_id)
        _design_mechanic.altitude_operating = 5
        _design_mechanic.rpm_operating = 81
        _design_mechanic = integration_test_table_model.do_select(self._update_id + 7)
        _design_mechanic.altitude_operating = 12
        _design_mechanic.rpm_operating = 71

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .altitude_operating
            == 5
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .rpm_operating
            == 81
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 7)
            .data[self._tag]
            .altitude_operating
            == 12
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 7)
            .data[self._tag]
            .rpm_operating
            == 71
        )

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _design_mechanic = integration_test_table_model.do_select(self._update_id)
        _design_mechanic.altitude_operating = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _design_mechanic = integration_test_table_model.do_select(self._update_id)
        _design_mechanic.altitude_operating = {1: 2}
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
class TestGetterSetterDesignMechanic(SystemTestGetterSetterMethods):
    """Class for testing Design Mechanic table getter and setter methods."""

    __test__ = True

    _package = {"rpm_design": 65.5}
    _record = RAMSTKDesignMechanicRecord
    _tag = "design_mechanic"
    _test_id = 8
