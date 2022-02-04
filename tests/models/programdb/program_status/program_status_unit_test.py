# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.program_status.program_status_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKProgramStatusRecord, RAMSTKProgramStatusTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramStatusTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_program_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_program_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_program_status")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_program_status_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_program_status")
    pub.unsubscribe(dut.do_insert, "request_insert_program_status")
    pub.unsubscribe(dut.do_get_actual_status, "request_get_actual_status")
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_program_remaining")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKProgramStatusRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_program_status"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.cost_remaining == 284.98
        assert test_recordmodel.date_status == date.today() - timedelta(days=1)
        assert test_recordmodel.time_remaining == 125.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKProgramStatusTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_status_id"
        assert test_tablemodel._db_tablename == "ramstk_program_status"
        assert test_tablemodel._tag == "program_status"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update, "request_update_program_status"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_program_statuss"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_program_status_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_program_status_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_program_status_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_delete, "request_delete_program_status"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_insert, "request_insert_program_status"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_actual_status, "request_get_actual_status"
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
            test_tablemodel.tree.get_node(1).data["program_status"],
            RAMSTKProgramStatusRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _status = test_tablemodel.do_select(2)

        assert isinstance(_status, RAMSTKProgramStatusRecord)
        assert _status.cost_remaining == 212.32
        assert _status.time_remaining == 112.5

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

        assert isinstance(_new_record, RAMSTKProgramStatusRecord)
        assert _new_record.revision_id == 1
        assert _new_record.status_id == 3
        assert _new_record.date_status == date.today()

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["program_status"],
            RAMSTKProgramStatusRecord,
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(2)

        assert test_tablemodel.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["cost_remaining"] == 284.98
        assert _attributes["date_status"] == date.today() - timedelta(days=1)
        assert _attributes["time_remaining"] == 125.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("status_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["time_remaining"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("status_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["time_remaining"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("status_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
