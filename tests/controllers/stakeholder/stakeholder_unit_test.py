# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.stakeholder.stakeholder_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKStakeholder
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amStakeholder, dmStakeholder
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture
def mock_program_dao(monkeypatch):
    _stakeholder_1 = MockRAMSTKStakeholder()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = "Stakeholder Input"
    _stakeholder_1.group = ""
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ""
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    _stakeholder_2 = MockRAMSTKStakeholder()
    _stakeholder_2.revision_id = 1
    _stakeholder_2.requirement_id = 1
    _stakeholder_2.stakeholder_id = 2
    _stakeholder_2.customer_rank = 1
    _stakeholder_2.description = "Stakeholder Input"
    _stakeholder_2.group = ""
    _stakeholder_2.improvement = 0.0
    _stakeholder_2.overall_weight = 0.0
    _stakeholder_2.planned_rank = 1
    _stakeholder_2.priority = 1
    _stakeholder_2.stakeholder = ""
    _stakeholder_2.user_float_1 = 1.0
    _stakeholder_2.user_float_2 = 1.0
    _stakeholder_2.user_float_3 = 1.0
    _stakeholder_2.user_float_4 = 1.0
    _stakeholder_2.user_float_5 = 1.0

    DAO = MockDAO()
    DAO.table = [
        _stakeholder_1,
        _stakeholder_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_analysismanager(test_toml_user_configuration):
    # Create the device under test (dut) and connect to the configuration.
    dut = amStakeholder(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_stakeholder_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_stakeholder_tree")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmStakeholder()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholders")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut._do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut._do_insert_stakeholder, "request_insert_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a Stakeholder data manager."""
        assert isinstance(test_datamanager, dmStakeholder)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._tag == "stakeholders"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_stakeholders"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_stakeholders"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_stakeholder_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_stakeholder_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_stakeholder_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager._do_delete, "request_delete_stakeholder"
        )
        assert pub.isSubscribed(
            test_datamanager._do_insert_stakeholder, "request_insert_stakeholder"
        )

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_analysismanager):
        """__init__() should create an instance of the function analysis
        manager."""
        assert isinstance(test_analysismanager, amStakeholder)
        assert isinstance(
            test_analysismanager.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration
        )
        assert isinstance(test_analysismanager._attributes, dict)
        assert isinstance(test_analysismanager._tree, Tree)
        assert test_analysismanager._attributes == {}
        assert pub.isSubscribed(
            test_analysismanager.on_get_all_attributes,
            "succeed_get_stakeholder_attributes",
        )
        assert pub.isSubscribed(
            test_analysismanager.on_get_tree, "succeed_get_stakeholder_tree"
        )
        assert pub.isSubscribed(
            test_analysismanager.do_calculate_stakeholder,
            "request_calculate_stakeholder",
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["stakeholder"], MockRAMSTKStakeholder)
        print("\033[36m\nsucceed_retrieve_stakeholders topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKStakeholder instances on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.tree.get_node(1).data, dict)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["stakeholder"], MockRAMSTKStakeholder
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKStakeholder on
        success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _stakeholder = test_datamanager.do_select(1, table="stakeholder")

        assert isinstance(_stakeholder, MockRAMSTKStakeholder)
        assert _stakeholder.description == "Stakeholder Input"
        assert _stakeholder.priority == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Stakeholder ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="stakeholder") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["stakeholder"], RAMSTKStakeholder)
        assert tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert (
            tree.get_node(3).data["stakeholder"].description == "New Stakeholder Input"
        )
        print("\033[36m\nsucceed_insert_stakeholder topic was broadcast")

    @pytest.mark.unit
    def test_do_insert(self, test_datamanager):
        """_do_insert_stakeholder() should send the success message after
        successfully inserting a new top-level stakeholder."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_stakeholder()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["stakeholder"], RAMSTKStakeholder
        )
        assert test_datamanager.tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert (
            test_datamanager.tree.get_node(3).data["stakeholder"].description
            == "New Stakeholder Input"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_improvement(self, test_analysismanager, test_datamanager):
        """do_calculate_stakeholder() should calculate the improvement factor
        and overall weight of a stakeholder input."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_get_tree()

        _stakeholder = test_datamanager.do_select(1, "stakeholder")
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        test_datamanager.do_update(1, table="stakeholder")
        test_datamanager.do_get_attributes(node_id=1, table="stakeholder")

        test_analysismanager.do_calculate_stakeholder(1)

        assert test_analysismanager._attributes["improvement"] == 1.2
        assert test_analysismanager._attributes["overall_weight"] == 12.48
