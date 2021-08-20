# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.similar_item.similar_item_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKSimilarItemRecord, RAMSTKSimilarItemTable

test_change_description = "Test change description for factor #1."


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSimilarItemTable()
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


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKSimilarItemRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_similar_item"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.hardware_id == 1
        assert test_recordmodel.change_description_1 == ""
        assert test_recordmodel.change_description_2 == ""
        assert test_recordmodel.change_description_3 == ""
        assert test_recordmodel.change_description_4 == ""
        assert test_recordmodel.change_description_5 == ""
        assert test_recordmodel.change_description_6 == ""
        assert test_recordmodel.change_description_7 == ""
        assert test_recordmodel.change_description_8 == ""
        assert test_recordmodel.change_description_9 == ""
        assert test_recordmodel.change_description_10 == ""
        assert test_recordmodel.change_factor_1 == 1.0
        assert test_recordmodel.change_factor_2 == 1.0
        assert test_recordmodel.change_factor_3 == 1.0
        assert test_recordmodel.change_factor_4 == 1.0
        assert test_recordmodel.change_factor_5 == 1.0
        assert test_recordmodel.change_factor_6 == 1.0
        assert test_recordmodel.change_factor_7 == 1.0
        assert test_recordmodel.change_factor_8 == 1.0
        assert test_recordmodel.change_factor_9 == 1.0
        assert test_recordmodel.change_factor_10 == 1.0
        assert test_recordmodel.environment_from_id == 0
        assert test_recordmodel.environment_to_id == 0
        assert test_recordmodel.function_1 == "0"
        assert test_recordmodel.function_2 == "0"
        assert test_recordmodel.function_3 == "0"
        assert test_recordmodel.function_4 == "0"
        assert test_recordmodel.function_5 == "0"
        assert test_recordmodel.parent_id == 0
        assert test_recordmodel.similar_item_method_id == 1
        assert test_recordmodel.quality_from_id == 0
        assert test_recordmodel.quality_to_id == 0
        assert test_recordmodel.result_1 == 0.0
        assert test_recordmodel.result_2 == 0.0
        assert test_recordmodel.result_3 == 0.0
        assert test_recordmodel.result_4 == 0.0
        assert test_recordmodel.result_5 == 0.0
        assert test_recordmodel.temperature_from == 30.0
        assert test_recordmodel.temperature_to == 30.0
        assert test_recordmodel.user_blob_1 == ""
        assert test_recordmodel.user_blob_2 == ""
        assert test_recordmodel.user_blob_3 == ""
        assert test_recordmodel.user_blob_4 == ""
        assert test_recordmodel.user_blob_5 == ""
        assert test_recordmodel.user_float_1 == 0.0
        assert test_recordmodel.user_float_2 == 0.0
        assert test_recordmodel.user_float_3 == 0.0
        assert test_recordmodel.user_float_4 == 0.0
        assert test_recordmodel.user_float_5 == 0.0
        assert test_recordmodel.user_int_1 == 0
        assert test_recordmodel.user_int_2 == 0
        assert test_recordmodel.user_int_3 == 0
        assert test_recordmodel.user_int_4 == 0
        assert test_recordmodel.user_int_5 == 0

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKSimilarItemTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_similar_item"
        assert test_tablemodel._tag == "similar_item"
        assert test_tablemodel._root == 0
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._record == RAMSTKSimilarItemRecord
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_similar_item_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_similar_item_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_tree, "succeed_calculate_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_similar_item_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update, "request_update_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_delete, "request_delete_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_insert, "request_insert_similar_item"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_roll_up_change_descriptions,
            "request_roll_up_change_descriptions",
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["similar_item"],
            RAMSTKSimilarItemRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _similar_item = test_tablemodel.do_select(1)

        assert isinstance(_similar_item, RAMSTKSimilarItemRecord)
        assert _similar_item.change_description_1 == ""
        assert _similar_item.temperature_from == 30.0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKSimilarItemRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 4

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["similar_item"],
            RAMSTKSimilarItemRecord,
        )
        assert test_tablemodel.tree.get_node(4).data["similar_item"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["similar_item"].hardware_id == 4
        assert test_tablemodel.tree.get_node(4).data["similar_item"].parent_id == 1


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(test_tablemodel.last_id)

        assert test_tablemodel.last_id == 2
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["change_description_1"] == ""
        assert _attributes["change_description_2"] == ""
        assert _attributes["change_description_3"] == ""
        assert _attributes["change_description_4"] == ""
        assert _attributes["change_description_5"] == ""
        assert _attributes["change_description_6"] == ""
        assert _attributes["change_description_7"] == ""
        assert _attributes["change_description_8"] == ""
        assert _attributes["change_description_9"] == ""
        assert _attributes["change_description_10"] == ""
        assert _attributes["change_factor_1"] == 1.0
        assert _attributes["change_factor_2"] == 1.0
        assert _attributes["change_factor_3"] == 1.0
        assert _attributes["change_factor_4"] == 1.0
        assert _attributes["change_factor_5"] == 1.0
        assert _attributes["change_factor_6"] == 1.0
        assert _attributes["change_factor_7"] == 1.0
        assert _attributes["change_factor_8"] == 1.0
        assert _attributes["change_factor_9"] == 1.0
        assert _attributes["change_factor_10"] == 1.0
        assert _attributes["environment_from_id"] == 0
        assert _attributes["environment_to_id"] == 0
        assert _attributes["function_1"] == "0"
        assert _attributes["function_2"] == "0"
        assert _attributes["function_3"] == "0"
        assert _attributes["function_4"] == "0"
        assert _attributes["function_5"] == "0"
        assert _attributes["parent_id"] == 0
        assert _attributes["similar_item_method_id"] == 1
        assert _attributes["quality_from_id"] == 0
        assert _attributes["quality_to_id"] == 0
        assert _attributes["result_1"] == 0.0
        assert _attributes["result_2"] == 0.0
        assert _attributes["result_3"] == 0.0
        assert _attributes["result_4"] == 0.0
        assert _attributes["result_5"] == 0.0
        assert _attributes["temperature_from"] == 30.0
        assert _attributes["temperature_to"] == 30.0
        assert _attributes["user_blob_1"] == ""
        assert _attributes["user_blob_2"] == ""
        assert _attributes["user_blob_3"] == ""
        assert _attributes["user_blob_4"] == ""
        assert _attributes["user_blob_5"] == ""
        assert _attributes["user_float_1"] == 0.0
        assert _attributes["user_float_2"] == 0.0
        assert _attributes["user_float_3"] == 0.0
        assert _attributes["user_float_4"] == 0.0
        assert _attributes["user_float_5"] == 0.0
        assert _attributes["user_int_1"] == 0
        assert _attributes["user_int_2"] == 0
        assert _attributes["user_int_3"] == 0
        assert _attributes["user_int_4"] == 0
        assert _attributes["user_int_5"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["function_1"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["function_1"] == "0"

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for similar item methods test suite."""

    @pytest.mark.unit
    def test_do_roll_up_change_descriptions(self, test_attributes, test_tablemodel):
        """should combine all child change descriptions into one for the parent."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _record = test_tablemodel.do_select(2)
        _record.change_description_1 = "This is change description 1 for assembly 2."
        _record.change_description_2 = "This is change description 2 for assembly 2."
        _record.change_description_3 = "This is change description 3 for assembly 2."

        _record = test_tablemodel.do_select(3)
        _record.change_description_1 = "This is change description 1 for assembly 3."
        _record.change_description_2 = "This is change description 2 for assembly 3."
        _record.change_description_3 = "This is change description 3 for assembly 3."

        test_tablemodel.do_roll_up_change_descriptions(1)

        _record = test_tablemodel.do_select(1)
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
    def test_do_calculate_topic_633(self, test_attributes, test_tablemodel):
        """should calculate the Topic 6.3.3 similar item."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel._node_hazard_rate = 0.000628

        _record = test_tablemodel.do_select(1)
        _record.similar_item_method_id = 1
        _record.change_description_1 = test_change_description
        _record.environment_from_id = 2
        _record.environment_to_id = 3
        _record.quality_from_id = 1
        _record.quality_to_id = 2
        _record.temperature_from = 55.0
        _record.temperature_to = 65.0

        test_tablemodel._do_calculate_topic_633(1)

        assert _record.change_factor_1 == 0.8
        assert _record.change_factor_2 == 1.4
        assert _record.change_factor_3 == 1.0
        assert _record.result_1 == pytest.approx(0.0005607143)
        assert _record.change_description_1 == test_change_description

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, test_attributes, test_tablemodel):
        """should calculate user-defined similar item."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel._node_hazard_rate = 0.000617

        _record = test_tablemodel.do_select(1)

        _record.similar_item_method_id = 2
        _record.change_description_1 = test_change_description
        _record.change_factor_1 = 0.85
        _record.change_factor_2 = 1.2
        _record.function_1 = "pi1*pi2*hr"
        _record.function_2 = "0"
        _record.function_3 = "0"
        _record.function_4 = "0"
        _record.function_5 = "0"

        test_tablemodel._do_calculate_user_defined(1)

        assert _record.change_description_1 == (test_change_description)
        assert _record.change_factor_1 == 0.85
        assert _record.change_factor_2 == 1.2
        assert _record.result_1 == pytest.approx(0.00062934)
