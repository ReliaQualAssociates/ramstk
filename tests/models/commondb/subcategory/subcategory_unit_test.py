# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.subcategory.subcategory_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing SubCategory module algorithms and models."""

# Third Party Imports
import pytest
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKSubCategoryRecord, RAMSTKSubCategoryTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSubCategoryTable()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_subcategory_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_subcategory_attributes")
    pub.unsubscribe(dut.do_update, "request_update_subcategory")
    pub.unsubscribe(dut.do_get_tree, "request_get_subcategory_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_subcategory_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKSubCategoryRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_subcategory"
        assert test_recordmodel.category_id == 1
        assert test_recordmodel.subcategory_id == 1
        assert test_recordmodel.description == "Linear"

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a SubCategory table model."""
        assert isinstance(test_tablemodel, RAMSTKSubCategoryTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._lst_id_columns == [
            "category_id",
            "subcategory_id",
        ]
        assert test_tablemodel._tag == "subcategory"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_subcategory_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_subcategory_tree"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSubCategoryRecord instances on success."""
        test_tablemodel.do_select_all({"category_id": 1})

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["subcategory"],
            RAMSTKSubCategoryRecord,
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKSubCategoryRecord record.
        assert len(test_tablemodel.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKSubCategoryRecord on
        success."""
        test_tablemodel.do_select_all({"subcategory_id": 1})

        _subcategory = test_tablemodel.do_select(1)

        assert isinstance(_subcategory, RAMSTKSubCategoryRecord)
        assert _subcategory.category_id == 1
        assert _subcategory.subcategory_id == 1
        assert _subcategory.description == "Linear"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all({"category_id": 1})

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_attributes(self, test_recordmodel):
        """get_attributes() should return a tuple of attribute values."""
        _attributes = test_recordmodel.get_attributes()
        assert _attributes["category_id"] == 1
        assert _attributes["subcategory_id"] == 1
        assert _attributes["description"] == "Linear"

    @pytest.mark.unit
    def test_set_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should return a zero error code on success."""
        test_attributes.pop("category_id")
        test_attributes.pop("subcategory_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, test_attributes, test_recordmodel):
        """set_attributes() should set an attribute to it's default value when the
        attribute is passed with a None value."""
        test_attributes["description"] = None

        test_attributes.pop("category_id")
        test_attributes.pop("subcategory_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert (
            test_recordmodel.get_attributes()["description"]
            == "Subcategory Description"
        )

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should raise an AttributeError when passed an unknown
        attribute."""
        test_attributes.pop("category_id")
        test_attributes.pop("subcategory_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
