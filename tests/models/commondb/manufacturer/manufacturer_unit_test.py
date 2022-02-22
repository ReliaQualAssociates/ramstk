# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.manufacturer.manufacturer_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Manufacturer module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKManufacturerRecord, RAMSTKManufacturerTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKManufacturerTable()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_manufacturer_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_manufacturer_attributes")
    pub.unsubscribe(dut.do_update, "request_update_manufacturer")
    pub.unsubscribe(dut.do_get_tree, "request_get_manufacturer_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_manufacturer_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKManufacturerRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_manufacturer"
        assert test_recordmodel.manufacturer_id == 1
        assert test_recordmodel.cage_code == "47278"
        assert test_recordmodel.description == "Eaton"
        assert test_recordmodel.location == "Cleveland, OH"

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a Manufacturer table model."""
        assert isinstance(test_tablemodel, RAMSTKManufacturerTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._lst_id_columns == [
            "manufacturer_id",
        ]
        assert test_tablemodel._tag == "manufacturer"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_manufacturer_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_manufacturer_tree"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKManufacturerRecord instances on success."""
        test_tablemodel.do_select_all({"manufacturer_id": 1})

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["manufacturer"],
            RAMSTKManufacturerRecord,
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKManufacturerRecord record.
        assert len(test_tablemodel.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKManufacturerRecord on
        success."""
        test_tablemodel.do_select_all({"manufacturer_id": 1})

        _manufacturer = test_tablemodel.do_select(1)

        assert isinstance(_manufacturer, RAMSTKManufacturerRecord)
        assert _manufacturer.manufacturer_id == 1
        assert _manufacturer.cage_code == "47278"
        assert _manufacturer.description == "Eaton"
        assert _manufacturer.location == "Cleveland, OH"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all({"manufacturer_id": 1})

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_attributes(self, test_recordmodel):
        """get_attributes() should return a tuple of attribute values."""
        _attributes = test_recordmodel.get_attributes()
        assert _attributes["manufacturer_id"] == 1
        assert _attributes["cage_code"] == "47278"
        assert _attributes["description"] == "Eaton"
        assert _attributes["location"] == "Cleveland, OH"

    @pytest.mark.unit
    def test_set_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should return a zero error code on success."""
        test_attributes.pop("manufacturer_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, test_attributes, test_recordmodel):
        """set_attributes() should set an attribute to it's default value when the
        attribute is passed with a None value."""
        test_attributes["cage_code"] = None

        test_attributes.pop("manufacturer_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["cage_code"] == "CAGE Code"

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should raise an AttributeError when passed an unknown
        attribute."""
        test_attributes.pop("manufacturer_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
