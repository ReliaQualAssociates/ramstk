# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Function algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKHazardAnalysis
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amHazards, dmHazards
from ramstk.models.programdb import RAMSTKHazardAnalysis


@pytest.fixture
def mock_program_dao(monkeypatch):
    _hazard_1 = MockRAMSTKHazardAnalysis()
    _hazard_1.revision_id = 1
    _hazard_1.function_id = 1
    _hazard_1.hazard_id = 1
    _hazard_1.assembly_effect = ""
    _hazard_1.assembly_hri = 20
    _hazard_1.assembly_hri_f = 4
    _hazard_1.assembly_mitigation = ""
    _hazard_1.assembly_probability = "Level A - Frequent"
    _hazard_1.assembly_probability_f = "Level B - Reasonably Probable"
    _hazard_1.assembly_severity = "Major"
    _hazard_1.assembly_severity_f = "Medium"
    _hazard_1.function_1 = "uf1*uf2"
    _hazard_1.function_2 = "res1/ui1"
    _hazard_1.function_3 = ""
    _hazard_1.function_4 = ""
    _hazard_1.function_5 = ""
    _hazard_1.potential_cause = ""
    _hazard_1.potential_hazard = ""
    _hazard_1.remarks = ""
    _hazard_1.result_1 = 0.0
    _hazard_1.result_2 = 0.0
    _hazard_1.result_3 = 0.0
    _hazard_1.result_4 = 0.0
    _hazard_1.result_5 = 0.0
    _hazard_1.system_effect = ""
    _hazard_1.system_hri = 20
    _hazard_1.system_hri_f = 20
    _hazard_1.system_mitigation = ""
    _hazard_1.system_probability = "Level A - Frequent"
    _hazard_1.system_probability_f = "Level C - Occasional"
    _hazard_1.system_severity = "Medium"
    _hazard_1.system_severity_f = "Medium"
    _hazard_1.user_blob_1 = ""
    _hazard_1.user_blob_2 = ""
    _hazard_1.user_blob_3 = ""
    _hazard_1.user_float_1 = 1.5
    _hazard_1.user_float_2 = 0.8
    _hazard_1.user_float_3 = 0.0
    _hazard_1.user_int_1 = 2
    _hazard_1.user_int_2 = 0
    _hazard_1.user_int_3 = 0

    DAO = MockDAO()
    DAO.table = [
        _hazard_1,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "function_id": 1,
        "hazard_id": 1,
    }


@pytest.fixture(scope="function")
def test_analysismanager(test_toml_user_configuration):
    """Get an analysis manager instance for each test function."""
    # Create the device under test (dut) and connect to the user configuration.
    dut = amHazards(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_hazard_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_hazard_tree")
    pub.unsubscribe(dut.do_calculate_fha, "request_calculate_fha")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmHazards()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hazard")
    pub.unsubscribe(dut.do_update, "request_update_hazard")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazard_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_set_all_attributes, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut.do_delete, "request_delete_hazard")
    pub.unsubscribe(dut.do_insert, "request_insert_hazard")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a Hazards data manager."""
        assert isinstance(test_datamanager, dmHazards)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_hazard_id"
        assert test_datamanager._db_tablename == "ramstk_hazard_analysis"
        assert test_datamanager._tag == "hazard"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_hazard")
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_hazard"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_hazard_attributes"
        )
        assert pub.isSubscribed(test_datamanager.do_get_tree, "request_get_hazard_tree")
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_hazard_attributes"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_hazard")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_hazard")

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_analysismanager):
        """__init__() should create an instance of the function analysis manager."""
        assert isinstance(test_analysismanager, amHazards)
        assert isinstance(
            test_analysismanager.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration
        )
        assert isinstance(test_analysismanager._attributes, dict)
        assert isinstance(test_analysismanager._tree, Tree)
        assert test_analysismanager._attributes == {}
        assert pub.isSubscribed(
            test_analysismanager.on_get_all_attributes, "succeed_get_hazard_attributes"
        )
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_get_hazard_tree"
        )
        assert pub.isSubscribed(
            test_analysismanager.do_calculate_fha, "request_calculate_fha"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with RAMSTKHazardAnalysis records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["hazard"], MockRAMSTKHazardAnalysis
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return an instance of the RAMSTKFunction on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _hazard = test_datamanager.do_select(1)

        assert isinstance(_hazard, MockRAMSTKHazardAnalysis)
        assert _hazard.assembly_hri_f == 4
        assert _hazard.assembly_probability == "Level A - Frequent"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """do_select() should return None when a non-existent Function ID is
        requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """_do_insert_hazard() should send the success message after successfully
        inserting a new hazard."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(2).data["hazard"], RAMSTKHazardAnalysis
        )
        assert test_datamanager.tree.get_node(2).data["hazard"].revision_id == 1
        assert test_datamanager.tree.get_node(2).data["hazard"].function_id == 1
        assert test_datamanager.tree.get_node(2).data["hazard"].hazard_id == 2


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_delete(1)

        assert test_datamanager.last_id == 0
        assert test_datamanager.tree.get_node(1) is None


@pytest.mark.usefixtures("test_analysismanager", "test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_hri(
        self, test_analysismanager, test_attributes, test_datamanager
    ):
        """do_calculate_hri() should calculate the hazard risk index hazard
        analysis."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _attributes = test_datamanager.do_select(1).get_attributes()

        test_analysismanager.on_get_all_attributes(_attributes)
        test_analysismanager._do_calculate_hri()

        assert test_analysismanager._attributes["assembly_hri"] == 30
        assert test_analysismanager._attributes["system_hri"] == 20
        assert test_analysismanager._attributes["assembly_hri_f"] == 16
        assert test_analysismanager._attributes["system_hri_f"] == 12

    @pytest.mark.unit
    def test_do_calculate_user_defined(
        self, test_analysismanager, test_attributes, test_datamanager
    ):
        """do_calculate_user_defined() should calculate the user-defined hazard
        analysis."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _attributes = test_datamanager.do_select(1).get_attributes()

        test_analysismanager.on_get_all_attributes(_attributes)
        test_analysismanager._do_calculate_user_defined()

        assert test_analysismanager._attributes["result_1"] == pytest.approx(1.2)
        assert test_analysismanager._attributes["result_2"] == pytest.approx(0.6)
