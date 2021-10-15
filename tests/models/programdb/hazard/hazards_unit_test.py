# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.hazards.hazards_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazard algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKHazardRecord, RAMSTKHazardTable

TEST_PROBS = {
    "A": "Level A - Frequent",
    "B": "Level B - Reasonably Probable",
    "C": "Level C - Occasional",
}


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKHazardTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_hazard_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_hazard")
    pub.unsubscribe(dut.do_update, "request_update_hazard")
    pub.unsubscribe(dut.do_get_tree, "request_get_hazard_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_set_attributes_all, "request_set_all_hazard_attributes")
    pub.unsubscribe(dut.do_delete, "request_delete_hazard")
    pub.unsubscribe(dut.do_insert, "request_insert_hazard")
    pub.unsubscribe(dut.do_calculate_fha, "request_calculate_fha")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKHazardRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_hazard_analysis"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.assembly_effect == ""
        assert test_recordmodel.assembly_hri == 20
        assert test_recordmodel.assembly_hri_f == 4
        assert test_recordmodel.assembly_mitigation == ""
        assert test_recordmodel.assembly_probability == TEST_PROBS["A"]
        assert test_recordmodel.assembly_probability_f == TEST_PROBS["B"]
        assert test_recordmodel.assembly_severity == "Major"
        assert test_recordmodel.assembly_severity_f == "Medium"
        assert test_recordmodel.function_1 == "uf1*uf2"
        assert test_recordmodel.function_2 == "res1/ui1"
        assert test_recordmodel.function_3 == ""
        assert test_recordmodel.function_4 == ""
        assert test_recordmodel.function_5 == ""
        assert test_recordmodel.potential_cause == ""
        assert test_recordmodel.potential_hazard == ""
        assert test_recordmodel.remarks == ""
        assert test_recordmodel.result_1 == 0.0
        assert test_recordmodel.result_2 == 0.0
        assert test_recordmodel.result_3 == 0.0
        assert test_recordmodel.result_4 == 0.0
        assert test_recordmodel.result_5 == 0.0
        assert test_recordmodel.system_effect == ""
        assert test_recordmodel.system_hri == 20
        assert test_recordmodel.system_hri_f == 20
        assert test_recordmodel.system_mitigation == ""
        assert test_recordmodel.system_probability == TEST_PROBS["A"]
        assert test_recordmodel.system_probability_f == TEST_PROBS["C"]
        assert test_recordmodel.system_severity == "Medium"
        assert test_recordmodel.system_severity_f == "Medium"
        assert test_recordmodel.user_blob_1 == ""
        assert test_recordmodel.user_blob_2 == ""
        assert test_recordmodel.user_blob_3 == ""
        assert test_recordmodel.user_float_1 == 1.5
        assert test_recordmodel.user_float_2 == 0.8
        assert test_recordmodel.user_float_3 == 0.0
        assert test_recordmodel.user_int_1 == 2
        assert test_recordmodel.user_int_2 == 0
        assert test_recordmodel.user_int_3 == 0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKHazardTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hazard_id"
        assert test_tablemodel._db_tablename == "ramstk_hazard_analysis"
        assert test_tablemodel._tag == "hazard"
        assert test_tablemodel._root == 0
        assert test_tablemodel._lst_id_columns == [
            "parent_id",
            "record_id",
            "revision_id",
            "function_id",
            "hazard_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKHazardRecord
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hazard_id"
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_hazard")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_hazard_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_hazard_tree")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_hazard")
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_hazard_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_hazard")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_hazard"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_fha, "request_calculate_fha"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing the select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["hazard"], RAMSTKHazardRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _hazard = test_tablemodel.do_select(1)

        assert isinstance(_hazard, RAMSTKHazardRecord)
        assert _hazard.hazard_id == 1
        assert _hazard.assembly_hri_f == 4
        assert _hazard.assembly_probability == "Level A - Frequent"

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

        assert isinstance(_new_record, RAMSTKHazardRecord)
        assert _new_record.revision_id == 1
        assert _new_record.function_id == 1
        assert _new_record.hazard_id == 2

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 2
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["hazard"], RAMSTKHazardRecord
        )
        assert test_tablemodel.tree.get_node(2).data["hazard"].revision_id == 1
        assert test_tablemodel.tree.get_node(2).data["hazard"].function_id == 1
        assert test_tablemodel.tree.get_node(2).data["hazard"].hazard_id == 2


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(1)

        assert test_tablemodel.last_id == 0
        assert test_tablemodel.tree.get_node(1) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["potential_hazard"] == ""
        assert _attributes["potential_cause"] == ""
        assert _attributes["assembly_effect"] == ""
        assert _attributes["assembly_severity"] == "Major"
        assert _attributes["assembly_probability"] == TEST_PROBS["A"]
        assert _attributes["assembly_hri"] == 20
        assert _attributes["assembly_mitigation"] == ""
        assert _attributes["assembly_severity_f"] == "Medium"
        assert _attributes["assembly_probability_f"] == TEST_PROBS["B"]
        assert _attributes["assembly_hri_f"] == 4
        assert _attributes["function_1"] == "uf1*uf2"
        assert _attributes["function_2"] == "res1/ui1"
        assert _attributes["function_3"] == ""
        assert _attributes["function_4"] == ""
        assert _attributes["function_5"] == ""
        assert _attributes["remarks"] == ""
        assert _attributes["result_1"] == 0.0
        assert _attributes["result_2"] == 0.0
        assert _attributes["result_3"] == 0.0
        assert _attributes["result_4"] == 0.0
        assert _attributes["result_5"] == 0.0
        assert _attributes["system_effect"] == ""
        assert _attributes["system_severity"] == "Medium"
        assert _attributes["system_probability"] == TEST_PROBS["A"]
        assert _attributes["system_hri"] == 20
        assert _attributes["system_mitigation"] == ""
        assert _attributes["system_severity_f"] == "Medium"
        assert _attributes["system_probability_f"] == TEST_PROBS["C"]
        assert _attributes["system_hri_f"] == 20
        assert _attributes["user_blob_1"] == ""
        assert _attributes["user_blob_2"] == ""
        assert _attributes["user_blob_3"] == ""
        assert _attributes["user_float_1"] == 1.5
        assert _attributes["user_float_2"] == 0.8
        assert _attributes["user_float_3"] == 0.0
        assert _attributes["user_int_1"] == 2
        assert _attributes["user_int_2"] == 0
        assert _attributes["user_int_3"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("hazard_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["system_hri_f"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("hazard_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["system_hri_f"] == 20

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("hazard_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_hri(self, test_attributes, test_tablemodel):
        """should calculate the hazard risk index (HRI) hazard analysis."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel._do_calculate_hri(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["assembly_hri"] == 30
        assert _attributes["system_hri"] == 20
        assert _attributes["assembly_hri_f"] == 16
        assert _attributes["system_hri_f"] == 12

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, test_attributes, test_tablemodel):
        """should calculate the user-defined hazard analysis."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel._do_calculate_user_defined(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["result_1"] == pytest.approx(1.2)
        assert _attributes["result_2"] == pytest.approx(0.6)

    @pytest.mark.unit
    def test_do_calculate_fha(self, test_attributes, test_tablemodel):
        """should calculate the HRI and user-defined hazard analyses."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel.do_calculate_fha(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["assembly_hri"] == 30
        assert _attributes["system_hri"] == 20
        assert _attributes["assembly_hri_f"] == 16
        assert _attributes["system_hri_f"] == 12
        assert _attributes["result_1"] == pytest.approx(1.2)
        assert _attributes["result_2"] == pytest.approx(0.6)
