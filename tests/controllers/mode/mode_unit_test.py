# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mode.mode_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure mode algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMode
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amMode, dmMode
from ramstk.models.programdb import RAMSTKMode


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mode_1 = MockRAMSTKMode()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ""
    _mode_1.mission = "Default Mission"
    _mode_1.other_indications = ""
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ""
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ""
    _mode_1.detection_method = ""
    _mode_1.operator_actions = ""
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ""
    _mode_1.severity_class = ""
    _mode_1.description = "Test Failure Mode #1"
    _mode_1.mission_phase = ""
    _mode_1.mode_probability = ""
    _mode_1.remarks = ""
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ""
    _mode_1.effect_end = ""
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.8

    _mode_2 = MockRAMSTKMode()
    _mode_2.revision_id = 1
    _mode_2.hardware_id = 1
    _mode_2.mode_id = 2
    _mode_2.effect_local = ""
    _mode_2.mission = "Default Mission"
    _mode_2.other_indications = ""
    _mode_2.mode_criticality = 0.0
    _mode_2.single_point = 0
    _mode_2.design_provisions = ""
    _mode_2.type_id = 0
    _mode_2.rpn_severity_new = 1
    _mode_2.effect_next = ""
    _mode_2.detection_method = ""
    _mode_2.operator_actions = ""
    _mode_2.critical_item = 0
    _mode_2.hazard_rate_source = ""
    _mode_2.severity_class = ""
    _mode_2.description = "Test Failure Mode #2"
    _mode_2.mission_phase = ""
    _mode_2.mode_probability = ""
    _mode_2.remarks = ""
    _mode_2.mode_ratio = 0.0
    _mode_2.mode_hazard_rate = 0.0
    _mode_2.rpn_severity = 1
    _mode_2.isolation_method = ""
    _mode_2.effect_end = ""
    _mode_2.mode_op_time = 0.0
    _mode_2.effect_probability = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mode_1,
        _mode_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_analysismanager(test_toml_user_configuration):
    """Get a analysis manager instance for each test function."""
    # Create the device under test (dut) and connect to the configuration.
    dut = amMode(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_tree, "succeed_retrieve_modes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_mode_tree")
    pub.unsubscribe(dut._do_calculate_criticality, "request_calculate_criticality")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMode()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mode")
    pub.unsubscribe(dut._do_insert_mode, "request_insert_mode")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should create a failure Mode data manager instance."""
        assert isinstance(test_datamanager, dmMode)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "mode"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_mode_attributes"
        )
        assert pub.isSubscribed(test_datamanager.do_get_tree, "request_get_mode_tree")
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_mode")
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_mode"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_mode")
        assert pub.isSubscribed(test_datamanager._do_insert_mode, "request_insert_mode")

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_analysismanager):
        """should create a failure Mode analysis manager instance."""
        assert isinstance(test_analysismanager, amMode)
        assert isinstance(
            test_analysismanager.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration
        )
        assert isinstance(test_analysismanager._attributes, dict)
        assert isinstance(test_analysismanager._tree, Tree)
        assert test_analysismanager._attributes == {}
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_retrieve_modes"
        )
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_get_mode_tree"
        )
        assert pub.isSubscribed(
            test_analysismanager._do_calculate_criticality,
            "request_calculate_criticality",
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """should return the records tree populated with RAMSTKMode instances."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["mode"], MockRAMSTKMode
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """should return an instance of the RAMSTKMode."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = test_datamanager.do_select(1, table="mode")

        assert isinstance(_mode, MockRAMSTKMode)
        assert _mode.effect_probability == 0.8
        assert _mode.description == "Test Failure Mode #1"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """should return None when a non-existent Mode ID is requested."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert test_datamanager.do_select(100, table="mode") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """should add the new node and update last_id."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager._do_insert_mode()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.tree.get_node(3).data["mode"], RAMSTKMode)
        assert test_datamanager.tree.get_node(3).data["mode"].mode_id == 3
        assert test_datamanager.tree.get_node(3).data["mode"].description is None


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove deleted mode from the records tree and update last_id."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager.do_delete(4)

        assert test_datamanager.tree.get_node(4) is None


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestAnalysisMethods:
    """Class for failure mode analysis manager method tests."""

    @pytest.mark.unit
    def test_do_calculate_criticality(self, test_analysismanager, test_datamanager):
        """should calculate the mode hazard rate and mode criticality."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        test_analysismanager._tree.get_node(1).data["mode"].mode_ratio = 0.428
        test_analysismanager._tree.get_node(1).data["mode"].mode_op_time = 4.2
        test_analysismanager._tree.get_node(1).data["mode"].effect_probability = 1.0
        test_analysismanager._tree.get_node(1).data["mode"].severity_class = "III"

        test_analysismanager._do_calculate_criticality(0.00000682)

        assert test_analysismanager._tree.get_node(1).data[
            "mode"
        ].mode_hazard_rate == pytest.approx(2.91896e-06)
        assert test_analysismanager._tree.get_node(1).data[
            "mode"
        ].mode_criticality == pytest.approx(1.2259632e-05)
