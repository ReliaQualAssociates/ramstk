# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.hardware.hardware_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import (
    RAMSTKDesignElectricRecord,
    RAMSTKDesignMechanicRecord,
    RAMSTKHardwareRecord,
    RAMSTKMilHdbk217FRecord,
    RAMSTKNSWCRecord,
    RAMSTKReliabilityRecord,
)
from ramstk.models.dbtables import RAMSTKHardwareTable
from ramstk.models.dbviews import RAMSTKHardwareBoMView


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
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
def test_viewmodel():
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHardwareBoMView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_all_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_electric")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_design_mechanic")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_reliability")
    pub.unsubscribe(dut.do_calculate_hardware, "request_calculate_hardware")
    pub.unsubscribe(dut.do_make_composite_ref_des, "request_make_comp_ref_des")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_attributes",
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
)
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hardware"], RAMSTKHardwareRecord)
        print("\033[36m\n\tsucceed_retrieve_hardware topic was broadcast.")

    def on_succeed_on_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hardware"], RAMSTKHardwareRecord)
        assert isinstance(
            tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            tree.get_node(1).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(tree.get_node(1).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        assert isinstance(tree.get_node(1).data["nswc"], RAMSTKNSWCRecord)
        assert isinstance(tree.get_node(1).data["reliability"], RAMSTKReliabilityRecord)
        print("\033[36m\n\tsucceed_retrieve_hardware_bom topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_hardware")

        test_tablemodel.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_hardware")

    @pytest.mark.integration
    def test_on_select_all(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should return records tree with hardware tables."""
        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_viewmodel.tree.get_node(1).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["reliability"],
            RAMSTKReliabilityRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(2).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(8).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(2).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

    @pytest.mark.integration
    def test_on_select_all_tree_loaded(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should clear existing nodes from the records tree and then re-populate."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert isinstance(
            test_viewmodel.tree.get_node(1).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.subscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

        test_viewmodel.on_select_all()

        assert isinstance(
            test_viewmodel.tree.get_node(1).data["hardware"],
            RAMSTKHardwareRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_electric"],
            RAMSTKDesignElectricRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["design_mechanic"],
            RAMSTKDesignMechanicRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_viewmodel.tree.get_node(1).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.unsubscribe(self.on_succeed_on_select_all, "succeed_retrieve_hardware_bom")

    @pytest.mark.integration
    def test_on_select_all_empty_base_tree(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should return an empty records tree if the base tree is empty."""
        test_viewmodel._dic_trees["hardware"] = Tree()

        assert test_viewmodel.on_select_all() is None
        assert test_viewmodel.tree.depth() == 0


@pytest.mark.usefixtures(
    "test_attributes",
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
)
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(9).data["hardware"], RAMSTKHardwareRecord)
        assert tree.get_node(9).data["hardware"].hardware_id == 9
        print("\033[36m\n\tsucceed_insert_hardware topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(9) is not present in table "
            '"ramstk_revision".'
        )
        print("\033[35m\n\tfail_insert_hardware topic was broadcast on no hardware.")

    def on_succeed_insert_hardware(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains(10)
        print(
            "\033[36m\n\tsucceed_insert_hardware topic was broadcast on hardware "
            "insert."
        )

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel, test_viewmodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_hardware")

        assert test_tablemodel.tree.get_node(9) is None

        test_attributes["hardware_id"] = 9
        test_attributes["record_id"] = 1
        pub.sendMessage("request_insert_hardware", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(9).data["hardware"],
            RAMSTKHardwareRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_hardware")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_hardware")

        assert test_tablemodel.tree.get_node(10) is None

        test_attributes["revision_id"] = 9
        test_attributes["record_id"] = 1
        pub.sendMessage("request_insert_hardware", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(10) is None

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_hardware")

    @pytest.mark.integration
    def test_do_insert_hardware(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should add a new hardware record to the view model records tree."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert not test_viewmodel.tree.contains(10)

        pub.subscribe(self.on_succeed_insert_hardware, "succeed_retrieve_hardware_bom")

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "parent_id": 0,
                "record_id": 1,
                "part": 0,
            },
        )

        pub.unsubscribe(
            self.on_succeed_insert_hardware, "succeed_retrieve_hardware_bom"
        )


@pytest.mark.usefixtures(
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_mechanic",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
)
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\n\tsucceed_delete_hardware topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hardware ID 300.")
        print(
            "\033[35m\n\tfail_delete_hardware topic was broadcast on non-existent ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Hardware ID 2.")
        print(
            "\033[35m\n\tfail_delete_hardware topic was broadcast on no data package."
        )

    def on_succeed_delete_hardware(self, tree):
        assert isinstance(tree, Tree)
        assert not tree.contains(5)
        print(
            "\033[36m\n\tsucceed_retrieve_hardware_bom topic was broadcast on hardware "
            "delete."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_hardware")

        _last_id = test_tablemodel.last_id
        pub.sendMessage("request_delete_hardware", node_id=_last_id)

        assert test_tablemodel.last_id == 7
        assert test_tablemodel.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_hardware")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_hardware")

        pub.sendMessage("request_delete_hardware", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_hardware")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_hardware")

        test_tablemodel.tree.get_node(2).data.pop("hardware")
        pub.sendMessage("request_delete_hardware", node_id=2)

        assert not isinstance(test_tablemodel.tree.get_node(6), RAMSTKHardwareRecord)
        assert not isinstance(test_tablemodel.tree.get_node(7), RAMSTKHardwareRecord)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_hardware")

    @pytest.mark.integration
    def test_do_delete_hardware(
        self,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should remove deleted hardware from records tree."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_design_mechanic.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1}
        )
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        assert test_viewmodel.tree.contains(5)

        pub.subscribe(self.on_succeed_delete_hardware, "succeed_retrieve_hardware_bom")

        pub.sendMessage("request_delete_hardware", node_id=5)

        pub.unsubscribe(
            self.on_succeed_delete_hardware, "succeed_retrieve_hardware_bom"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["hardware"].parent_id == 1
        assert tree.get_node(2).data["hardware"].total_power_dissipation == 0.5
        assert (
            tree.get_node(2).data["hardware"].specification_number
            == "Big Specification"
        )
        print("\033[36m\n\tsucceed_update_hardware topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for Hardware.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for hardware ID 1 was the "
            "wrong type."
        )
        print(
            "\033[35m\n\tfail_update_hardware topic was broadcast on wrong data type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\n\tfail_update_hardware topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent hardware with hardware ID 100."
        )
        print(
            "\033[35m\n\tfail_update_hardware topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for hardware ID 1.")
        print(
            "\033[35m\n\tfail_update_hardware topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_hardware")

        _hardware = test_tablemodel.do_select(2)
        _hardware.total_power_dissipation = 0.5
        _hardware.specification_number = "Big Specification"
        pub.sendMessage("request_update_hardware", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_hardware")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_hardware")

        _hardware = test_tablemodel.do_select(1)
        _hardware.total_power_dissipation = 5
        _hardware.specification_number = "81"
        _hardware = test_tablemodel.do_select(2)
        _hardware.total_power_dissipation = 12
        _hardware.specification_number = "71"

        pub.sendMessage("request_update_all_hardware")

        assert (
            test_tablemodel.tree.get_node(1).data["hardware"].total_power_dissipation
            == 5
        )
        assert (
            test_tablemodel.tree.get_node(1).data["hardware"].specification_number
            == "81"
        )
        assert (
            test_tablemodel.tree.get_node(2).data["hardware"].total_power_dissipation
            == 12
        )
        assert (
            test_tablemodel.tree.get_node(2).data["hardware"].specification_number
            == "71"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_hardware")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_hardware")

        _hardware = test_tablemodel.do_select(1)
        _hardware.specification_number = {1: 2}
        pub.sendMessage("request_update_hardware", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_hardware")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_hardware",
        )

        _hardware = test_tablemodel.do_select(1)
        _hardware.specification_number = {1: 2}
        pub.sendMessage("request_update_hardware", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type,
            "fail_update_hardware",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_hardware")

        pub.sendMessage("request_update_hardware", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_hardware")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_hardware")

        test_tablemodel.tree.get_node(1).data.pop("hardware")
        pub.sendMessage("request_update_hardware", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_hardware")


@pytest.mark.usefixtures("test_tablemodel", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 2
        assert attributes["alt_part_number"] == ""
        assert attributes["attachments"] == ""
        assert attributes["cage_code"] == ""
        assert attributes["category_id"] == 0
        assert attributes["comp_ref_des"] == "S1:SS1"
        assert attributes["cost"] == 0.0
        assert attributes["cost_failure"] == 0.0
        assert attributes["cost_hour"] == 0.0
        assert attributes["cost_type_id"] == 0
        assert attributes["description"] == "Test Sub-System 1"
        assert attributes["duty_cycle"] == 100.0
        assert attributes["figure_number"] == ""
        assert attributes["lcn"] == ""
        assert attributes["level"] == 0
        assert attributes["manufacturer_id"] == 0
        assert attributes["mission_time"] == 100.0
        assert attributes["name"] == ""
        assert attributes["nsn"] == ""
        assert attributes["page_number"] == ""
        assert attributes["parent_id"] == 1
        assert attributes["part"] == 0
        assert attributes["part_number"] == ""
        assert attributes["quantity"] == 1
        assert attributes["ref_des"] == "SS1"
        assert attributes["remarks"] == ""
        assert attributes["repairable"] == 0
        assert attributes["specification_number"] == ""
        assert attributes["subcategory_id"] == 0
        assert attributes["tagged_part"] == 0
        assert attributes["total_cost"] == 0.0
        assert attributes["total_part_count"] == 0
        assert attributes["total_power_dissipation"] == 0.0
        assert attributes["year_of_manufacture"] == 2019
        print("\033[36m\n\tsucceed_get_hardware_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["hardware"], RAMSTKHardwareRecord)
        print("\033[36m\n\tsucceed_get_hardware_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["hardware"].cage_code == "DE34T1"
        print("\033[36m\n\tsucceed_get_hardware_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_hardware_attributes")

        test_tablemodel.do_get_attributes(node_id=2)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_hardware_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_hardware_tree"
        )

        pub.sendMessage("request_get_hardware_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_hardware_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_hardware_tree")

        pub.sendMessage(
            "request_set_hardware_attributes",
            node_id=2,
            package={"cage_code": "DE34T1"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_hardware_tree")


@pytest.mark.usefixtures(
    "test_tablemodel",
    "test_viewmodel",
    "test_design_electric",
    "test_design_electric",
    "test_milhdbk217f",
    "test_nswc",
    "test_reliability",
    "test_toml_user_configuration",
)
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.integration
    def test_do_calculate_power_dissipation_part(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should calculate the total power dissipation of a part."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.part = 1
        _hardware.quantity = 2

        _design_electric = test_design_electric.do_select(8)
        _design_electric.power_operating = 0.00295

        test_viewmodel.do_calculate_power_dissipation(8)
        _attributes = test_tablemodel.do_select(8).get_attributes()

        assert _attributes["total_power_dissipation"] == 0.0059

    @pytest.mark.skip
    @pytest.mark.integration
    def test_do_calculate_power_dissipation_assembly(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """should calculate the total power dissipation of an assembly."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(2)
        _hardware.part = 0
        _hardware.quantity = 1
        _hardware = test_tablemodel.do_select(6)
        _hardware.part = 0
        _hardware.quantity = 4
        _hardware = test_tablemodel.do_select(7)
        _hardware.part = 1
        _hardware.quantity = 3

        _design_electric = test_design_electric.do_select(7)
        _design_electric.power_operating = 0.00295

        test_viewmodel.do_calculate_power_dissipation(2)
        _attributes = test_tablemodel.do_select(2).get_attributes()

        assert _attributes["total_power_dissipation"] == 0.00885

    @pytest.mark.integration
    def test_do_calculate_part_stress(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_stress_limits,
    ):
        """calculate part stress ratios and check derating limits."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.subcategory_id = 2

        _hardware = test_reliability.do_select(8)
        _hardware.quality_id = 3

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 3
        _hardware.power_operating = 0.03
        _hardware.power_rated = 0.1
        _hardware.temperature_case = 46.9
        _hardware.temperature_knee = 85.0
        _hardware.temperature_rated_max = 150.0
        _hardware.voltage_operating = 3.3
        _hardware.voltage_rated = 5.0

        test_viewmodel._dic_stress_limits = test_stress_limits
        test_viewmodel.do_calculate_part_stress(8)

        assert _hardware.overstress == 0
        assert _hardware.reason == ""

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_mil_hdbk_217f(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_stress_limits,
    ):
        """predict the active hazard of a part using MIL-HDBK-217F."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.subcategory_id = 1
        _hardware.part = 1

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 9

        _hardware = test_milhdbk217f.do_select(8)
        _hardware.piR = 0.0038

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 1
        _hardware.hazard_rate_method_id = 2
        _hardware.quality_id = 3

        test_viewmodel._dic_stress_limits = test_stress_limits
        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(0.003995836)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_specified_hazard_rate(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """predict the active hazard of an assembly with specified hazard rate.."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.000007829

        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(7.829e-06)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_part_specified_mtbf(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """predict the active hazard of an assembly with specified MTBF."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 3
        _hardware.mtbf_specified = 127730.0

        test_viewmodel.do_calculate_hardware(8)
        _attributes = test_reliability.do_select(8).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(7.8290143e-06)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_assessed(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_toml_user_configuration,
    ):
        """predict the active hazard of an assembly by sum of children."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        test_design_electric._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )

        _hardware = test_tablemodel.do_select(1)
        _hardware.quantity = 1
        _hardware.part = 0

        _hardware = test_reliability.do_select(1)
        _hardware.hazard_rate_type_id = 1

        _hardware = test_tablemodel.do_select(2)
        _hardware.quantity = 2
        _hardware.part = 0

        _hardware = test_reliability.do_select(2)
        _hardware.hazard_rate_type_id = 1

        for _id in [3, 4, 5, 6, 7]:
            _hardware = test_tablemodel.do_select(_id)
            _hardware.quantity = 1
            _hardware.part = 0

            _hardware = test_reliability.do_select(_id)
            _hardware.hazard_rate_type_id = 2
            _hardware.hazard_rate_specified = 0.0001 * (_id - 2)

        _hardware = test_reliability.do_select(7)
        _hardware.hazard_rate_type_id = 1

        _hardware = test_tablemodel.do_select(8)
        _hardware.quantity = 1
        _hardware.part = 1

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.000004815

        test_viewmodel.do_calculate_hardware(1)

        _attributes = test_reliability.do_select(8).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.000004815)

        _attributes = test_reliability.do_select(7).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.000004815)

        _attributes = test_reliability.do_select(6).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0004)

        _attributes = test_reliability.do_select(5).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0003)

        _attributes = test_reliability.do_select(4).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0002)

        _attributes = test_reliability.do_select(3).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.0001)

        _attributes = test_reliability.do_select(2).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00080963)

        _attributes = test_reliability.do_select(1).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.00140963)

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_specified_hazard_rate(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """predict the active hazard of an assembly with specified hazard rate."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(5)
        _hardware.quantity = 1
        _hardware.part = 0

        _hardware = test_reliability.do_select(5)
        _hardware.hazard_rate_type_id = 2
        _hardware.hazard_rate_specified = 0.0007829

        test_viewmodel.do_calculate_hardware(5)

        _attributes = test_reliability.do_select(5).get_attributes()
        assert _attributes["hazard_rate_active"] == 0.0007829

    @pytest.mark.integration
    def test_do_predict_hazard_rate_active_assembly_specified_mtbf(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
    ):
        """predict the active hazard of an assembly with specified MTBF."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        _hardware = test_tablemodel.do_select(2)
        _hardware.quantity = 3
        _hardware.part = 0

        _hardware = test_reliability.do_select(2)
        _hardware.hazard_rate_type_id = 3
        _hardware.mtbf_specified = 10000.0

        test_viewmodel.do_calculate_hardware(2)
        _attributes = test_reliability.do_select(2).get_attributes()

        assert _attributes["hazard_rate_active"] == pytest.approx(0.0003)

    @pytest.mark.integration
    def test_do_calculate_hardware(
        self,
        test_attributes,
        test_tablemodel,
        test_viewmodel,
        test_design_electric,
        test_design_mechanic,
        test_milhdbk217f,
        test_nswc,
        test_reliability,
        test_toml_user_configuration,
    ):
        """calculate all hardware metrics for a part."""
        test_tablemodel.do_select_all(attributes={"revision_id": 1})
        test_design_electric.do_select_all(attributes={"revision_id": 1})
        test_design_mechanic.do_select_all(attributes={"revision_id": 1})
        test_milhdbk217f.do_select_all(attributes={"revision_id": 1})
        test_nswc.do_select_all(attributes={"revision_id": 1})
        test_reliability.do_select_all(attributes={"revision_id": 1})

        test_design_electric._dic_stress_limits = (
            test_toml_user_configuration.RAMSTK_STRESS_LIMITS
        )

        _hardware = test_tablemodel.do_select(8)
        _hardware.category_id = 3
        _hardware.cost = 12.98
        _hardware.cost_type_id = 2
        _hardware.part = 1
        _hardware.quantity = 2
        _hardware.subcategory_id = 1

        _hardware = test_design_electric.do_select(8)
        _hardware.environment_active_id = 9
        _hardware.environment_dormant_id = 1
        _hardware.power_operating = 0.00295

        _hardware = test_milhdbk217f.do_select(8)
        _hardware.piR = 0.0038

        _hardware = test_reliability.do_select(8)
        _hardware.hazard_rate_type_id = 1
        _hardware.hazard_rate_method_id = 1
        _hardware.quality_id = 3

        test_viewmodel.do_calculate_hardware(8)

        _attributes = test_tablemodel.do_select(8).get_attributes()
        assert _attributes["total_cost"] == 25.96
        assert _attributes["total_part_count"] == 2
        assert _attributes["total_power_dissipation"] == 0.0059

        _attributes = test_reliability.do_select(8).get_attributes()
        assert _attributes["hazard_rate_active"] == pytest.approx(0.015)
        assert _attributes["hazard_rate_dormant"] == pytest.approx(0.0009)
        assert _attributes["hazard_rate_logistics"] == pytest.approx(0.0159)
        assert _attributes["hazard_rate_mission"] == pytest.approx(1.4109)
        assert _attributes["mtbf_logistics"] == pytest.approx(62893081.7610063)
        assert _attributes["mtbf_mission"] == pytest.approx(708767.4533985)
        assert _attributes["reliability_logistics"] == pytest.approx(0.9999984)
        assert _attributes["reliability_mission"] == pytest.approx(0.9998589)
