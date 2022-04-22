# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.status.status_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStatusRecord
from ramstk.models.dbtables import RAMSTKStatusTable
from tests import MockDAO


@pytest.fixture(scope="function")
def test_tablemodel(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStatusTable()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_status")
    pub.unsubscribe(dut.do_get_tree, "request_get_status_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_status_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKStatusRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_status"
        assert test_record_model.status_id == 1
        assert test_record_model.status_type == "action"
        assert test_record_model.name == "Initiated"
        assert test_record_model.description == "Action has been initiated."

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a Status table model."""
        assert isinstance(test_tablemodel, RAMSTKStatusTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._lst_id_columns == [
            "status_id",
        ]
        assert test_tablemodel._tag == "status"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_status_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_status_tree")


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKStatusRecord instances on success."""
        test_tablemodel.do_select_all({"status_id": 1})

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["status"], RAMSTKStatusRecord
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKStatusRecord record.
        assert len(test_tablemodel.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKStatusRecord on
        success."""
        test_tablemodel.do_select_all({"status_id": 1})

        _status = test_tablemodel.do_select(1)

        assert isinstance(_status, RAMSTKStatusRecord)
        assert _status.status_id == 1
        assert _status.status_type == "action"
        assert _status.name == "Initiated"
        assert _status.description == "Action has been initiated."

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all({"status_id": 1})

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """get_attributes() should return a tuple of attribute values."""
        _attributes = test_record_model.get_attributes()
        assert _attributes["status_id"] == 1
        assert _attributes["status_type"] == "action"
        assert _attributes["name"] == "Initiated"
        assert _attributes["description"] == "Action has been initiated."

    @pytest.mark.unit
    def test_set_attributes(self, test_attributes, test_record_model):
        """set_attributes() should return a zero error code on success."""
        test_attributes.pop("status_id")
        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, test_attributes, test_record_model):
        """set_attributes() should set an attribute to it's default value when the
        attribute is passed with a None value."""
        test_attributes["name"] = None

        test_attributes.pop("status_id")
        assert test_record_model.set_attributes(test_attributes) is None
        assert test_record_model.get_attributes()["name"] == "Status Name"

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(
        self, test_attributes, test_record_model
    ):
        """set_attributes() should raise an AttributeError when passed an unknown
        attribute."""
        test_attributes.pop("status_id")
        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})
