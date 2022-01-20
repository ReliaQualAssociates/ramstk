# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opload.opload_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Load algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKOpLoadRecord, RAMSTKOpLoadTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpLoadTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKOpLoadRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_op_load"
        assert test_recordmodel.damage_model == 3
        assert test_recordmodel.description == "Test Operating Load #1"
        assert test_recordmodel.priority_id == 0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_tablemodel, RAMSTKOpLoadTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_load_id"
        assert test_tablemodel._db_tablename == "ramstk_op_load"
        assert test_tablemodel._tag == "opload"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_opload_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_opload_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_set_attributes, "wvw_editing_opload")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_opload")
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_opload_tree")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_opload")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_opload")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoadRecord instances on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["opload"], RAMSTKOpLoadRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return an instance of the RAMSTKOpLoadRecord on
        success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _opload = test_tablemodel.do_select(2)

        assert isinstance(_opload, RAMSTKOpLoadRecord)
        assert _opload.description == "Test Operating Load #2"
        assert _opload.priority_id == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent opload ID is
        requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """_do_insert_opload() should send the success message after successfully
        inserting an operating load."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["opload"], RAMSTKOpLoadRecord
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
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
        assert _attributes["description"] == "Test Operating Load #1"
        assert _attributes["damage_model"] == 3
        assert _attributes["priority_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("load_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to its default value when passed a None value."""
        test_attributes["priority_id"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("load_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["priority_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("load_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
