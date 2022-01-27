# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.action.action_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKActionRecord, RAMSTKActionTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKActionTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut.do_insert, "request_insert_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKActionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_action"
        assert (
            test_recordmodel.action_recommended
            == "Test FMEA Action #1 for Cause ID #3."
        )
        assert test_recordmodel.action_category == "Detection"
        assert test_recordmodel.action_owner == ""
        assert test_recordmodel.action_due_date == date.today() + timedelta(days=30)
        assert test_recordmodel.action_status == ""
        assert test_recordmodel.action_taken == ""
        assert test_recordmodel.action_approved == 0
        assert test_recordmodel.action_approve_date == date.today() + timedelta(days=30)
        assert test_recordmodel.action_closed == 0
        assert test_recordmodel.action_close_date == date.today() + timedelta(days=30)

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_tablemodel, RAMSTKActionTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_action_id"
        assert test_tablemodel._db_tablename == "ramstk_action"
        assert test_tablemodel._tag == "action"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_action_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_action_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_set_attributes, "wvw_editing_action")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_action")
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_action_tree")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_action")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_action")


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """should return a Tree() object populated with RAMSTKActionRecord
        instances."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["action"], RAMSTKActionRecord
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["action"], RAMSTKActionRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """should return an instance of the RAMSTKActionRecord on success."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        _action = test_tablemodel.do_select(1)

        assert isinstance(_action, RAMSTKActionRecord)
        assert _action.action_recommended == "Test FMEA Action #1 for Cause ID #3."
        assert _action.action_category == "Detection"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """should return None when a non-existent action ID is requested."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        test_tablemodel.do_select_all(test_attributes)
        test_tablemodel.do_insert(test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["action"], RAMSTKActionRecord
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_tablemodel.do_delete(2)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert (
            _attributes["action_recommended"] == "Test FMEA Action #1 for Cause ID #3."
        )
        assert _attributes["action_taken"] == ""

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        test_attributes.pop("action_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["action_category"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        test_attributes.pop("action_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["action_category"] == ""

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        test_attributes.pop("action_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
