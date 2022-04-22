# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.group.group_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Group module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKGroupRecord
from ramstk.models.dbtables import RAMSTKGroupTable
from tests import MockDAO


@pytest.fixture(scope="function")
def test_tablemodel(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKGroupTable()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_group_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_group_attributes")
    pub.unsubscribe(dut.do_update, "request_update_group")
    pub.unsubscribe(dut.do_get_tree, "request_get_group_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_group_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKGroupRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_group"
        assert test_record_model.group_id == 1
        assert test_record_model.group_type == "work"
        assert test_record_model.description == "Engineering, RMS"

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a Group table model."""
        assert isinstance(test_tablemodel, RAMSTKGroupTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._lst_id_columns == [
            "group_id",
        ]
        assert test_tablemodel._tag == "group"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_group_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_group_tree")


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKGroupRecord instances on success."""
        test_tablemodel.do_select_all({"group_id": 1})

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["group"], RAMSTKGroupRecord
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKGroupRecord record.
        assert len(test_tablemodel.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKGroupRecord on
        success."""
        test_tablemodel.do_select_all({"group_id": 1})

        _group = test_tablemodel.do_select(1)

        assert isinstance(_group, RAMSTKGroupRecord)
        assert _group.group_id == 1
        assert _group.group_type == "work"
        assert _group.description == "Engineering, RMS"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all({"group_id": 1})

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """get_attributes() should return a tuple of attribute values."""
        _attributes = test_record_model.get_attributes()
        assert _attributes["group_id"] == 1
        assert _attributes["group_type"] == "work"
        assert _attributes["description"] == "Engineering, RMS"

    @pytest.mark.unit
    def test_set_attributes(self, test_attributes, test_record_model):
        """set_attributes() should return a zero error code on success."""
        test_attributes.pop("group_id")
        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, test_attributes, test_record_model):
        """set_attributes() should set an attribute to it's default value when the
        attribute is passed with a None value."""
        test_attributes["group_type"] = None

        test_attributes.pop("group_id")
        assert test_record_model.set_attributes(test_attributes) is None
        assert test_record_model.get_attributes()["group_type"] == ""

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(
        self, test_attributes, test_record_model
    ):
        """set_attributes() should raise an AttributeError when passed an unknown
        attribute."""
        test_attributes.pop("group_id")
        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})
