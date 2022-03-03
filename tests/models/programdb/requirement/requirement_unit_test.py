# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.requirement.requirement_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRequirementRecord
from ramstk.models.dbtables import RAMSTKRequirementTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKRequirementTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_requirement")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_requirement")
    pub.unsubscribe(dut.do_update, "request_update_requirement")
    pub.unsubscribe(dut.do_create_all_codes, "request_create_all_requirement_codes")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_requirement_tree")
    pub.unsubscribe(dut.do_create_code, "request_create_requirement_code")
    pub.unsubscribe(dut.do_delete, "request_delete_requirement")
    pub.unsubscribe(dut.do_insert, "request_insert_requirement")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKRequirementRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_requirement"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.derived == 0
        assert test_recordmodel.description == ""
        assert test_recordmodel.figure_number == ""
        assert test_recordmodel.owner == 0
        assert test_recordmodel.page_number == ""
        assert test_recordmodel.parent_id == 0
        assert test_recordmodel.priority == 0
        assert test_recordmodel.requirement_code == "REL.1"
        assert test_recordmodel.specification == ""
        assert test_recordmodel.requirement_type == 0
        assert test_recordmodel.validated == 0
        assert test_recordmodel.validated_date == date.today()
        assert test_recordmodel.q_clarity_0 == 0
        assert test_recordmodel.q_clarity_1 == 0
        assert test_recordmodel.q_clarity_2 == 0
        assert test_recordmodel.q_clarity_3 == 0
        assert test_recordmodel.q_clarity_4 == 0
        assert test_recordmodel.q_clarity_5 == 0
        assert test_recordmodel.q_clarity_6 == 0
        assert test_recordmodel.q_clarity_7 == 0
        assert test_recordmodel.q_clarity_8 == 0
        assert test_recordmodel.q_complete_0 == 0
        assert test_recordmodel.q_complete_1 == 0
        assert test_recordmodel.q_complete_2 == 0
        assert test_recordmodel.q_complete_3 == 0
        assert test_recordmodel.q_complete_4 == 0
        assert test_recordmodel.q_complete_5 == 0
        assert test_recordmodel.q_complete_6 == 0
        assert test_recordmodel.q_complete_7 == 0
        assert test_recordmodel.q_complete_8 == 0
        assert test_recordmodel.q_complete_9 == 0
        assert test_recordmodel.q_consistent_0 == 0
        assert test_recordmodel.q_consistent_1 == 0
        assert test_recordmodel.q_consistent_2 == 0
        assert test_recordmodel.q_consistent_3 == 0
        assert test_recordmodel.q_consistent_4 == 0
        assert test_recordmodel.q_consistent_5 == 0
        assert test_recordmodel.q_consistent_6 == 0
        assert test_recordmodel.q_consistent_7 == 0
        assert test_recordmodel.q_consistent_8 == 0
        assert test_recordmodel.q_verifiable_0 == 0
        assert test_recordmodel.q_verifiable_1 == 0
        assert test_recordmodel.q_verifiable_2 == 0
        assert test_recordmodel.q_verifiable_3 == 0
        assert test_recordmodel.q_verifiable_4 == 0
        assert test_recordmodel.q_verifiable_5 == 0

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a Requirement data manager."""
        assert isinstance(test_tablemodel, RAMSTKRequirementTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_requirement_id"
        assert test_tablemodel._db_tablename == "ramstk_requirement"
        assert test_tablemodel._tag == "requirement"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_requirement")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_requirement"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_requirement_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_requirement_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_requirement_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_requirement"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_create_code, "request_create_requirement_code"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_requirement")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_requirement")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree object populated with
        RAMSTKRequirementRecord instances on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.tree.get_node(1).data, dict)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["requirement"],
            RAMSTKRequirementRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return an instance of the RAMSTKRequirementRecord on
        success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _requirement = test_tablemodel.do_select(1)

        assert isinstance(_requirement, RAMSTKRequirementRecord)
        assert _requirement.description == ""
        assert _requirement.priority == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent Requirement ID is
        requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message after successfully inserting a
        new top-level requirement."""
        test_attributes["record_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["requirement"],
            RAMSTKRequirementRecord,
        )
        assert test_tablemodel.tree.get_node(3).data["requirement"].requirement_id == 3
        assert (
            test_tablemodel.tree.get_node(3).data["requirement"].description
            == "New Requirement"
        )

    @pytest.mark.unit
    def test_do_insert_child(self, test_attributes, test_tablemodel):
        """do_insert() should send the success message after successfully inserting a
        new child requirement."""
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["requirement"],
            RAMSTKRequirementRecord,
        )
        assert test_tablemodel.tree.get_node(3).data["requirement"].parent_id == 1
        assert test_tablemodel.tree.get_node(3).data["requirement"].requirement_id == 3
        assert (
            test_tablemodel.tree.get_node(3).data["requirement"].description
            == "New Requirement"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """_do_delete() should send the success message with the treelib Tree."""
        test_attributes["record_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(test_tablemodel.last_id)

        assert test_tablemodel.last_id == 1


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["derived"] == 0
        assert _attributes["description"] == ""
        assert _attributes["figure_number"] == ""
        assert _attributes["owner"] == 0
        assert _attributes["page_number"] == ""
        assert _attributes["parent_id"] == 0
        assert _attributes["priority"] == 0
        assert _attributes["requirement_code"] == "REL.1"
        assert _attributes["specification"] == ""
        assert _attributes["requirement_type"] == 0
        assert _attributes["validated"] == 0
        assert _attributes["validated_date"] == date.today()
        assert _attributes["q_clarity_0"] == 0
        assert _attributes["q_clarity_1"] == 0
        assert _attributes["q_clarity_2"] == 0
        assert _attributes["q_clarity_3"] == 0
        assert _attributes["q_clarity_4"] == 0
        assert _attributes["q_clarity_5"] == 0
        assert _attributes["q_clarity_6"] == 0
        assert _attributes["q_clarity_7"] == 0
        assert _attributes["q_clarity_8"] == 0
        assert _attributes["q_complete_0"] == 0
        assert _attributes["q_complete_1"] == 0
        assert _attributes["q_complete_2"] == 0
        assert _attributes["q_complete_3"] == 0
        assert _attributes["q_complete_4"] == 0
        assert _attributes["q_complete_5"] == 0
        assert _attributes["q_complete_6"] == 0
        assert _attributes["q_complete_7"] == 0
        assert _attributes["q_complete_8"] == 0
        assert _attributes["q_complete_9"] == 0
        assert _attributes["q_consistent_0"] == 0
        assert _attributes["q_consistent_1"] == 0
        assert _attributes["q_consistent_2"] == 0
        assert _attributes["q_consistent_3"] == 0
        assert _attributes["q_consistent_4"] == 0
        assert _attributes["q_consistent_5"] == 0
        assert _attributes["q_consistent_6"] == 0
        assert _attributes["q_consistent_7"] == 0
        assert _attributes["q_consistent_8"] == 0
        assert _attributes["q_verifiable_0"] == 0
        assert _attributes["q_verifiable_1"] == 0
        assert _attributes["q_verifiable_2"] == 0
        assert _attributes["q_verifiable_3"] == 0
        assert _attributes["q_verifiable_4"] == 0
        assert _attributes["q_verifiable_5"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["priority"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["priority"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
