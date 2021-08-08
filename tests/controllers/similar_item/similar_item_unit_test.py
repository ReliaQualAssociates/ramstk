# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.similar_item.similar_item_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKSimilarItem
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmSimilarItem
from ramstk.models.programdb import RAMSTKSimilarItem


@pytest.fixture
def mock_program_dao(monkeypatch):
    _similar_item_1 = MockRAMSTKSimilarItem()
    _similar_item_1.revision_id = 1
    _similar_item_1.hardware_id = 1
    _similar_item_1.change_description_1 = ""
    _similar_item_1.change_description_2 = ""
    _similar_item_1.change_description_3 = ""
    _similar_item_1.change_description_4 = ""
    _similar_item_1.change_description_5 = ""
    _similar_item_1.change_description_6 = ""
    _similar_item_1.change_description_7 = ""
    _similar_item_1.change_description_8 = ""
    _similar_item_1.change_description_9 = ""
    _similar_item_1.change_description_10 = ""
    _similar_item_1.change_factor_1 = 1.0
    _similar_item_1.change_factor_2 = 1.0
    _similar_item_1.change_factor_3 = 1.0
    _similar_item_1.change_factor_4 = 1.0
    _similar_item_1.change_factor_5 = 1.0
    _similar_item_1.change_factor_6 = 1.0
    _similar_item_1.change_factor_7 = 1.0
    _similar_item_1.change_factor_8 = 1.0
    _similar_item_1.change_factor_9 = 1.0
    _similar_item_1.change_factor_10 = 1.0
    _similar_item_1.environment_from_id = 0
    _similar_item_1.environment_to_id = 0
    _similar_item_1.function_1 = "0"
    _similar_item_1.function_2 = "0"
    _similar_item_1.function_3 = "0"
    _similar_item_1.function_4 = "0"
    _similar_item_1.function_5 = "0"
    _similar_item_1.parent_id = 0
    _similar_item_1.similar_item_method_id = 1
    _similar_item_1.quality_from_id = 0
    _similar_item_1.quality_to_id = 0
    _similar_item_1.result_1 = 0.0
    _similar_item_1.result_2 = 0.0
    _similar_item_1.result_3 = 0.0
    _similar_item_1.result_4 = 0.0
    _similar_item_1.result_5 = 0.0
    _similar_item_1.temperature_from = 30.0
    _similar_item_1.temperature_to = 30.0
    _similar_item_1.user_blob_1 = ""
    _similar_item_1.user_blob_2 = ""
    _similar_item_1.user_blob_3 = ""
    _similar_item_1.user_blob_4 = ""
    _similar_item_1.user_blob_5 = ""
    _similar_item_1.user_float_1 = 0.0
    _similar_item_1.user_float_2 = 0.0
    _similar_item_1.user_float_3 = 0.0
    _similar_item_1.user_float_4 = 0.0
    _similar_item_1.user_float_5 = 0.0
    _similar_item_1.user_int_1 = 0
    _similar_item_1.user_int_2 = 0
    _similar_item_1.user_int_3 = 0
    _similar_item_1.user_int_4 = 0
    _similar_item_1.user_int_5 = 0

    _similar_item_2 = MockRAMSTKSimilarItem()
    _similar_item_2.revision_id = 1
    _similar_item_2.hardware_id = 2
    _similar_item_2.change_description_1 = ""
    _similar_item_2.change_description_2 = ""
    _similar_item_2.change_description_3 = ""
    _similar_item_2.change_description_4 = ""
    _similar_item_2.change_description_5 = ""
    _similar_item_2.change_description_6 = ""
    _similar_item_2.change_description_7 = ""
    _similar_item_2.change_description_8 = ""
    _similar_item_2.change_description_9 = ""
    _similar_item_2.change_description_10 = ""
    _similar_item_2.change_factor_1 = 1.0
    _similar_item_2.change_factor_2 = 1.0
    _similar_item_2.change_factor_3 = 1.0
    _similar_item_2.change_factor_4 = 1.0
    _similar_item_2.change_factor_5 = 1.0
    _similar_item_2.change_factor_6 = 1.0
    _similar_item_2.change_factor_7 = 1.0
    _similar_item_2.change_factor_8 = 1.0
    _similar_item_2.change_factor_9 = 1.0
    _similar_item_2.change_factor_10 = 1.0
    _similar_item_2.environment_from_id = 0
    _similar_item_2.environment_to_id = 0
    _similar_item_2.function_1 = "0"
    _similar_item_2.function_2 = "0"
    _similar_item_2.function_3 = "0"
    _similar_item_2.function_4 = "0"
    _similar_item_2.function_5 = "0"
    _similar_item_2.parent_id = 1
    _similar_item_2.similar_item_method_id = 1
    _similar_item_2.quality_from_id = 0
    _similar_item_2.quality_to_id = 0
    _similar_item_2.result_1 = 0.0
    _similar_item_2.result_2 = 0.0
    _similar_item_2.result_3 = 0.0
    _similar_item_2.result_4 = 0.0
    _similar_item_2.result_5 = 0.0
    _similar_item_2.temperature_from = 30.0
    _similar_item_2.temperature_to = 30.0
    _similar_item_2.user_blob_1 = ""
    _similar_item_2.user_blob_2 = ""
    _similar_item_2.user_blob_3 = ""
    _similar_item_2.user_blob_4 = ""
    _similar_item_2.user_blob_5 = ""
    _similar_item_2.user_float_1 = 0.0
    _similar_item_2.user_float_2 = 0.0
    _similar_item_2.user_float_3 = 0.0
    _similar_item_2.user_float_4 = 0.0
    _similar_item_2.user_float_5 = 0.0
    _similar_item_2.user_int_1 = 0
    _similar_item_2.user_int_2 = 0
    _similar_item_2.user_int_3 = 0
    _similar_item_2.user_int_4 = 0
    _similar_item_2.user_int_5 = 0

    _similar_item_3 = MockRAMSTKSimilarItem()
    _similar_item_3.revision_id = 1
    _similar_item_3.hardware_id = 3
    _similar_item_3.change_description_1 = ""
    _similar_item_3.change_description_2 = ""
    _similar_item_3.change_description_3 = ""
    _similar_item_3.change_description_4 = ""
    _similar_item_3.change_description_5 = ""
    _similar_item_3.change_description_6 = ""
    _similar_item_3.change_description_7 = ""
    _similar_item_3.change_description_8 = ""
    _similar_item_3.change_description_9 = ""
    _similar_item_3.change_description_10 = ""
    _similar_item_3.change_factor_1 = 1.0
    _similar_item_3.change_factor_2 = 1.0
    _similar_item_3.change_factor_3 = 1.0
    _similar_item_3.change_factor_4 = 1.0
    _similar_item_3.change_factor_5 = 1.0
    _similar_item_3.change_factor_6 = 1.0
    _similar_item_3.change_factor_7 = 1.0
    _similar_item_3.change_factor_8 = 1.0
    _similar_item_3.change_factor_9 = 1.0
    _similar_item_3.change_factor_10 = 1.0
    _similar_item_3.environment_from_id = 0
    _similar_item_3.environment_to_id = 0
    _similar_item_3.function_1 = "0"
    _similar_item_3.function_2 = "0"
    _similar_item_3.function_3 = "0"
    _similar_item_3.function_4 = "0"
    _similar_item_3.function_5 = "0"
    _similar_item_3.parent_id = 1
    _similar_item_3.similar_item_method_id = 1
    _similar_item_3.quality_from_id = 0
    _similar_item_3.quality_to_id = 0
    _similar_item_3.result_1 = 0.0
    _similar_item_3.result_2 = 0.0
    _similar_item_3.result_3 = 0.0
    _similar_item_3.result_4 = 0.0
    _similar_item_3.result_5 = 0.0
    _similar_item_3.temperature_from = 30.0
    _similar_item_3.temperature_to = 30.0
    _similar_item_3.user_blob_1 = ""
    _similar_item_3.user_blob_2 = ""
    _similar_item_3.user_blob_3 = ""
    _similar_item_3.user_blob_4 = ""
    _similar_item_3.user_blob_5 = ""
    _similar_item_3.user_float_1 = 0.0
    _similar_item_3.user_float_2 = 0.0
    _similar_item_3.user_float_3 = 0.0
    _similar_item_3.user_float_4 = 0.0
    _similar_item_3.user_float_5 = 0.0
    _similar_item_3.user_int_1 = 0
    _similar_item_3.user_int_2 = 0
    _similar_item_3.user_int_3 = 0
    _similar_item_3.user_int_4 = 0
    _similar_item_3.user_int_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _similar_item_1,
        _similar_item_2,
        _similar_item_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 4,
        "parent_id": 1,
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmSimilarItem()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_similar_item_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_similar_item_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_similar_item")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_similar_item")
    pub.unsubscribe(dut.do_update, "request_update_similar_item")
    pub.unsubscribe(dut.do_get_tree, "request_get_similar_item_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_similar_item")
    pub.unsubscribe(dut.do_insert, "request_insert_similar_item")
    pub.unsubscribe(dut.do_calculate_similar_item, "request_calculate_similar_item")
    pub.unsubscribe(
        dut.do_roll_up_change_descriptions, "request_roll_up_change_descriptions"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a table manager instance."""
        assert isinstance(test_datamanager, dmSimilarItem)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._db_id_colname == "fld_hardware_id"
        assert test_datamanager._db_tablename == "ramstk_similar_item"
        assert test_datamanager._tag == "similar_item"
        assert test_datamanager._root == 0
        assert test_datamanager._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_datamanager._record == RAMSTKSimilarItem
        assert test_datamanager.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_similar_item_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_similar_item_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_tree, "succeed_calculate_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_similar_item_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_delete, "request_delete_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_insert, "request_insert_similar_item"
        )
        assert pub.isSubscribed(
            test_datamanager.do_roll_up_change_descriptions,
            "request_roll_up_change_descriptions",
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with DB records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["similar_item"],
            MockRAMSTKSimilarItem,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return the record for the passed record ID."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _similar_item = test_datamanager.do_select(1)

        assert isinstance(_similar_item, MockRAMSTKSimilarItem)
        assert _similar_item.change_description_1 == ""
        assert _similar_item.temperature_from == 30.0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """should return None when a non-existent record ID is requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_datamanager):
        """should return a new record instance with ID fields populated."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _new_record = test_datamanager.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKSimilarItem)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 4

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a new record to the records tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)

        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(4).data["similar_item"], RAMSTKSimilarItem
        )
        assert test_datamanager.tree.get_node(4).data["similar_item"].revision_id == 1
        assert test_datamanager.tree.get_node(4).data["similar_item"].hardware_id == 4
        assert test_datamanager.tree.get_node(4).data["similar_item"].parent_id == 1


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _last_id = test_datamanager.last_id
        test_datamanager.do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 2
        assert test_datamanager.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for similar item methods test suite."""

    @pytest.mark.unit
    def test_do_roll_up_change_descriptions(self, test_attributes, test_datamanager):
        """should combine all child change descriptions into one for the parent."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _record = test_datamanager.do_select(2)
        _record.change_description_1 = "This is change description 1 for assembly 2."
        _record.change_description_2 = "This is change description 2 for assembly 2."
        _record.change_description_3 = "This is change description 3 for assembly 2."

        _record = test_datamanager.do_select(3)
        _record.change_description_1 = "This is change description 1 for assembly 3."
        _record.change_description_2 = "This is change description 2 for assembly 3."
        _record.change_description_3 = "This is change description 3 for assembly 3."

        test_datamanager.do_roll_up_change_descriptions(1)

        _record = test_datamanager.do_select(1)
        assert _record.change_description_1 == (
            "This is change description 1 for assembly 2.\n\nThis is change "
            "description 1 for assembly 3.\n\n"
        )
        assert _record.change_description_2 == (
            "This is change description 2 for assembly 2.\n\nThis is change "
            "description 2 for assembly 3.\n\n"
        )
        assert _record.change_description_3 == (
            "This is change description 3 for assembly 2.\n\nThis is change "
            "description 3 for assembly 3.\n\n"
        )

    @pytest.mark.unit
    def test_do_calculate_topic_633(self, test_attributes, test_datamanager):
        """should calculate the Topic 6.3.3 similar item."""
        test_datamanager.do_select_all(attributes=test_attributes)

        test_datamanager._node_hazard_rate = 0.000628

        _record = test_datamanager.do_select(1)
        _record.similar_item_method_id = 1
        _record.change_description_1 = "Test change description for factor #1."
        _record.environment_from_id = 2
        _record.environment_to_id = 3
        _record.quality_from_id = 1
        _record.quality_to_id = 2
        _record.temperature_from = 55.0
        _record.temperature_to = 65.0

        test_datamanager._do_calculate_topic_633(1)

        assert _record.change_factor_1 == 0.8
        assert _record.change_factor_2 == 1.4
        assert _record.change_factor_3 == 1.0
        assert _record.result_1 == pytest.approx(0.0005607143)
        assert _record.change_description_1 == "Test change description for factor #1."

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, test_attributes, test_datamanager):
        """should calculate user-defined similar item."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager._node_hazard_rate = 0.000617

        _record = test_datamanager.do_select(1)

        _record.similar_item_method_id = 2
        _record.change_description_1 = "Test change description for factor #1."
        _record.change_factor_1 = 0.85
        _record.change_factor_2 = 1.2
        _record.function_1 = "pi1*pi2*hr"
        _record.function_2 = "0"
        _record.function_3 = "0"
        _record.function_4 = "0"
        _record.function_5 = "0"

        test_datamanager._do_calculate_user_defined(1)

        assert _record.change_description_1 == (
            "Test change description for factor #1."
        )
        assert _record.change_factor_1 == 0.85
        assert _record.change_factor_2 == 1.2
        assert _record.result_1 == pytest.approx(0.00062934)
