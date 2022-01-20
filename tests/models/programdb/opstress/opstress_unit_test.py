# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opstress.opstress_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Stress algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKOpStressRecord, RAMSTKOpStressTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKOpStressTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opstress")
    pub.unsubscribe(dut.do_insert, "request_insert_opstress")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKOpStressRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_op_stress"
        assert test_recordmodel.description == "Test Operating Stress #1"
        assert test_recordmodel.load_history == 2
        assert test_recordmodel.measurable_parameter == 0
        assert test_recordmodel.remarks == ""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_tablemodel, RAMSTKOpStressTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_stress_id"
        assert test_tablemodel._db_tablename == "ramstk_op_stress"
        assert test_tablemodel._tag == "opstress"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_opstress_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_opstress_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_opstress"
        )
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_opstress")
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_opstress_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_opstress")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_opstress")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpStressRecord instances on success."""
        test_tablemodel.do_select_all(test_attributes)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["opstress"], RAMSTKOpStressRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return an instance of the RAMSTKOpStressRecord on
        success."""
        test_tablemodel.do_select_all(test_attributes)
        _opstress = test_tablemodel.do_select(2)

        assert isinstance(_opstress, RAMSTKOpStressRecord)
        assert _opstress.description == "Test Operating Stress #2"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent opstress ID is
        requested."""
        test_tablemodel.do_select_all(test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """_do_insert_opstress() should send the success message after successfully
        inserting an operating load."""
        test_tablemodel.do_select_all(test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["opstress"], RAMSTKOpStressRecord
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
        test_tablemodel.do_select_all(test_attributes)
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
        assert _attributes["description"] == "Test Operating Stress #1"
        assert _attributes["load_history"] == 2
        assert _attributes["measurable_parameter"] == 0
        assert _attributes["remarks"] == ""

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("load_id")
        test_attributes.pop("stress_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["measurable_parameter"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("load_id")
        test_attributes.pop("stress_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["measurable_parameter"] == 0

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
        test_attributes.pop("stress_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
