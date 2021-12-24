# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.reliability.reliability_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Reliability module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKReliabilityRecord, RAMSTKReliabilityTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKReliabilityTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_reliability_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_reliability_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_reliability")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_reliability")
    pub.unsubscribe(dut.do_update, "request_update_reliability")
    pub.unsubscribe(dut.do_get_tree, "request_get_reliability_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_reliability")
    pub.unsubscribe(dut.do_insert, "request_insert_reliability")
    pub.unsubscribe(
        dut.do_calculate_hazard_rate_active, "request_calculate_hazard_rate_active"
    )
    pub.unsubscribe(
        dut.do_calculate_hazard_rate_dormant,
        "request_calculate_hazard_rate_dormant",
    )
    pub.unsubscribe(
        dut.do_calculate_hazard_rate_logistics,
        "request_calculate_hazard_rate_logistics",
    )
    pub.unsubscribe(
        dut.do_calculate_hazard_rate_mission, "request_calculate_hazard_rate_mission"
    )
    pub.unsubscribe(dut.do_calculate_mtbf, "request_calculate_mtbf")
    pub.unsubscribe(dut.do_calculate_reliability, "request_calculate_reliability")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["reliability"], RAMSTKReliabilityRecord)
        print("\033[36m\nsucceed_retrieve_reliability topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_reliability")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_reliability")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(8).data["reliability"], RAMSTKReliabilityRecord)
        assert tree.get_node(8).data["reliability"].hardware_id == 8
        print("\033[36m\nsucceed_insert_reliability topic was broadcast.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(9) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_reliability topic was broadcast on no hardware.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_reliability")

        assert test_tablemodel.tree.get_node(8) is None

        test_attributes["hardware_id"] = 8
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 8
        pub.sendMessage("request_insert_reliability", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(8).data["reliability"],
            RAMSTKReliabilityRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_reliability")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_reliability")

        assert test_tablemodel.tree.get_node(9) is None

        test_attributes["hardware_id"] = 9
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 9
        pub.sendMessage("request_insert_reliability", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(9) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_reliability")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_reliability topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Reliability ID 300.")
        print(
            "\033[35m\nfail_delete_reliability topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Reliability ID 2.")
        print(
            "\033[35m\nfail_delete_reliability topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_reliability")

        _last_id = test_tablemodel.last_id
        pub.sendMessage("request_delete_reliability", node_id=_last_id)

        assert test_tablemodel.last_id == 6
        assert test_tablemodel.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_reliability")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_reliability")

        pub.sendMessage("request_delete_reliability", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_reliability")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_reliability")

        test_tablemodel.tree.get_node(2).data.pop("reliability")
        pub.sendMessage("request_delete_reliability", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_reliability")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["reliability"].category_id == 5
        assert tree.get_node(2).data["reliability"].subcategory_id == 81
        print("\033[36m\nsucceed_update_reliability topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast for Reliability.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for reliability "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_reliability topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_reliability topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent reliability with reliability "
            "ID 100."
        )
        print(
            "\033[35m\nfail_update_reliability topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for reliability ID 1."
        )
        print(
            "\033[35m\nfail_update_reliability topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_reliability")

        _reliability = test_tablemodel.do_select(2)
        _reliability.category_id = 5
        _reliability.subcategory_id = 81
        pub.sendMessage("request_update_reliability", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_reliability")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _reliability = test_tablemodel.do_select(1)
        _reliability.category_id = 5
        _reliability.subcategory_id = 81
        _reliability = test_tablemodel.do_select(2)
        _reliability.category_id = 12
        _reliability.subcategory_id = 71

        pub.sendMessage("request_update_all_reliability")

        assert test_tablemodel.tree.get_node(1).data["reliability"].category_id == 5
        assert test_tablemodel.tree.get_node(1).data["reliability"].subcategory_id == 81
        assert test_tablemodel.tree.get_node(2).data["reliability"].category_id == 12
        assert test_tablemodel.tree.get_node(2).data["reliability"].subcategory_id == 71

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_reliability")

        _reliability = test_tablemodel.do_select(1)
        _reliability.hazard_rate_active = {1: 2}
        pub.sendMessage("request_update_reliability", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_reliability")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_reliability"
        )

        _reliability = test_tablemodel.do_select(1)
        _reliability.hazard_rate_dormant = {1: 2}
        pub.sendMessage("request_update_reliability", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_reliability"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_reliability")

        pub.sendMessage("request_update_reliability", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_reliability")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_reliability")

        test_tablemodel.tree.get_node(1).data.pop("reliability")
        pub.sendMessage("request_update_reliability", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_reliability")


@pytest.mark.usefixtures("test_tablemodel", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 2
        assert attributes["add_adj_factor"] == 0.0
        assert attributes["availability_logistics"] == 1.0
        assert attributes["availability_mission"] == 1.0
        assert attributes["avail_log_variance"] == 0.0
        assert attributes["avail_mis_variance"] == 0.0
        assert attributes["failure_distribution_id"] == 0
        assert attributes["hazard_rate_active"] == 0.00617
        assert attributes["hazard_rate_dormant"] == 0.0
        assert attributes["hazard_rate_logistics"] == 0.0
        assert attributes["hazard_rate_method_id"] == 0
        assert attributes["hazard_rate_mission"] == 0.0
        assert attributes["hazard_rate_model"] == ""
        assert attributes["hazard_rate_percent"] == 0.0
        assert attributes["hazard_rate_software"] == 0.0
        assert attributes["hazard_rate_specified"] == 0.0
        assert attributes["hazard_rate_type_id"] == 0
        assert attributes["hr_active_variance"] == 0.0
        assert attributes["hr_dormant_variance"] == 0.0
        assert attributes["hr_logistics_variance"] == 0.0
        assert attributes["hr_mission_variance"] == 0.0
        assert attributes["hr_specified_variance"] == 0.0
        assert attributes["lambda_b"] == 0.0
        assert attributes["location_parameter"] == 0.0
        assert attributes["mtbf_logistics"] == 0.0
        assert attributes["mtbf_mission"] == 0.0
        assert attributes["mtbf_specified"] == 0.0
        assert attributes["mtbf_logistics_variance"] == 0.0
        assert attributes["mtbf_mission_variance"] == 0.0
        assert attributes["mtbf_specified_variance"] == 0.0
        assert attributes["mult_adj_factor"] == 1.0
        assert attributes["quality_id"] == 0
        assert attributes["reliability_goal"] == 0.0
        assert attributes["reliability_goal_measure_id"] == 0
        assert attributes["reliability_logistics"] == 1.0
        assert attributes["reliability_mission"] == 1.0
        assert attributes["reliability_log_variance"] == 0.0
        assert attributes["reliability_miss_variance"] == 0.0
        assert attributes["scale_parameter"] == 0.0
        assert attributes["shape_parameter"] == 0.0
        assert attributes["survival_analysis_id"] == 0

        print("\033[36m\nsucceed_get_reliability_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["reliability"], RAMSTKReliabilityRecord)
        print("\033[36m\nsucceed_get_reliability_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["reliability"].location_parameter == 65.5
        print("\033[36m\nsucceed_get_reliability_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_reliability_attributes"
        )

        test_tablemodel.do_get_attributes(
            node_id=2,
            table="reliability",
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_reliability_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_reliability_tree"
        )

        pub.sendMessage("request_get_reliability_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_reliability_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_reliability_tree")

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[2],
            package={"location_parameter": 65.5},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_reliability_tree")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_request_predict_hazard_rate(self, node_id):
        assert node_id == 1
        print("\033[36m\nrequest_predict_active_hazard_rate topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_hazard_rate_active_predict(self, test_tablemodel):
        """should calculate the active hazard rate."""
        pub.subscribe(
            self.on_request_predict_hazard_rate, "request_predict_active_hazard_rate"
        )

        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 1
        _reliability.hazard_rate_specified = 0.000056

        pub.sendMessage(
            "request_calculate_hazard_rate_active",
            node_id=1,
            duty_cycle=100.0,
            quantity=1,
            multiplier=1.0,
            time=0.0,
        )

        pub.unsubscribe(
            self.on_request_predict_hazard_rate, "request_predict_active_hazard_rate"
        )

    @pytest.mark.integration
    def test_do_calculate_hazard_rate_active(self, test_tablemodel):
        """should calculate the active hazard rate."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_specified = 0.000056

        pub.sendMessage(
            "request_calculate_hazard_rate_active",
            node_id=1,
            duty_cycle=100.0,
            quantity=1,
            multiplier=1.0,
            time=0.0,
        )

        assert _reliability.hazard_rate_active == 0.000056

    @pytest.mark.integration
    def test_do_calculate_hazard_rate_dormant(self, test_tablemodel):
        """should calculate the dormant hazard rate."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_active = 0.000056

        pub.sendMessage(
            "request_calculate_hazard_rate_dormant",
            node_id=1,
            category_id=2,
            subcategory_id=2,
            env_active=3,
            env_dormant=2,
        )

        assert _reliability.hazard_rate_dormant == 2.24e-06

    @pytest.mark.integration
    def test_do_calculate_hazard_rate_logistics(self, test_tablemodel):
        """should calculate the logistics hazard rate."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_active = 0.000056
        _reliability.hazard_rate_dormant = 2.24e-06
        _reliability.hazard_rate_software = 0.000032

        pub.sendMessage(
            "request_calculate_hazard_rate_logistics",
            node_id=1,
        )

        assert _reliability.hazard_rate_logistics == 9.024e-05

    @pytest.mark.integration
    def test_do_calculate_hazard_rate_mission(self, test_tablemodel):
        """should calculate the mission hazard rate."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_active = 0.000056
        _reliability.hazard_rate_dormant = 2.24e-06
        _reliability.hazard_rate_software = 0.000032

        pub.sendMessage(
            "request_calculate_hazard_rate_mission",
            node_id=1,
            duty_cycle=0.35,
        )

        assert _reliability.hazard_rate_mission == 5.3056e-05

    @pytest.mark.integration
    def test_do_calculate_mtbf(self, test_tablemodel):
        """should calculate the logistics and mission mtbf."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_logistics = 9.024e-05
        _reliability.hazard_rate_mission = 5.3056e-05

        pub.sendMessage(
            "request_calculate_mtbf",
            node_id=1,
            multiplier=1.0,
        )

        assert _reliability.mtbf_logistics == pytest.approx(11081.5602837)
        assert _reliability.mtbf_mission == pytest.approx(18848.0096502)

    @pytest.mark.integration
    def test_do_calculate_reliability(self, test_tablemodel):
        """should calculate the logistics and mission reliability."""
        _reliability = test_tablemodel.do_select(1)
        _reliability.hardware_id = 1
        _reliability.hazard_rate_type_id = 2
        _reliability.hazard_rate_logistics = 9.024e-05
        _reliability.hazard_rate_mission = 5.3056e-05

        pub.sendMessage(
            "request_calculate_reliability",
            node_id=1,
            time=1.0,
        )

        assert _reliability.reliability_logistics == pytest.approx(0.9999098)
        assert _reliability.reliability_mission == pytest.approx(0.9999469)
