# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.function.function_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKFunctionRecord, RAMSTKFunctionTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFunctionTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_function")
    pub.unsubscribe(dut.do_update, "request_update_function")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_function_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_function")
    pub.unsubscribe(dut.do_insert, "request_insert_function")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKFunctionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_function"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.availability_logistics == 1.0
        assert test_recordmodel.availability_mission == 1.0
        assert test_recordmodel.cost == 0.0
        assert test_recordmodel.function_code == "PRESS-001"
        assert test_recordmodel.hazard_rate_logistics == 0.0
        assert test_recordmodel.hazard_rate_mission == 0.0
        assert test_recordmodel.level == 0
        assert test_recordmodel.mmt == 0.0
        assert test_recordmodel.mcmt == 0.0
        assert test_recordmodel.mpmt == 0.0
        assert test_recordmodel.mtbf_logistics == 0.0
        assert test_recordmodel.mtbf_mission == 0.0
        assert test_recordmodel.mttr == 0.0
        assert test_recordmodel.name == "Function Name"
        assert test_recordmodel.parent_id == 0
        assert test_recordmodel.remarks == ""
        assert test_recordmodel.safety_critical == 0
        assert test_recordmodel.total_mode_count == 0
        assert test_recordmodel.total_part_count == 0
        assert test_recordmodel.type_id == 0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a Function data manager."""
        assert isinstance(test_tablemodel, RAMSTKFunctionTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_function_id"
        assert test_tablemodel._db_tablename == "ramstk_function"
        assert test_tablemodel._tag == "function"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_function")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_functions"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_function_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_function_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_function_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_function")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_function")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], RAMSTKFunctionRecord)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return record tree populated with RAMSTKFunctionRecord records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["function"], RAMSTKFunctionRecord
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["function"], RAMSTKFunctionRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the RAMSTKFunctionRecord record for the requested Function
        ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _function = test_tablemodel.do_select(1)

        assert isinstance(_function, RAMSTKFunctionRecord)
        assert _function.availability_logistics == 1.0
        assert _function.name == "Function Name"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent Function ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["function"], RAMSTKFunctionRecord
        )
        assert test_tablemodel.tree.get_node(3).data["function"].function_id == 3
        assert test_tablemodel.tree.get_node(3).data["function"].name == "New Function"

    @pytest.mark.unit
    def test_do_insert_child(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_attributes["parent_id"] = 2
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["function"], RAMSTKFunctionRecord
        )
        assert test_tablemodel.tree.get_node(3).data["function"].function_id == 3
        assert test_tablemodel.tree.get_node(3).data["function"].name == "New Function"
        assert test_tablemodel.tree.get_node(3).data["function"].parent_id == 2


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove a record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(test_tablemodel.last_id)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["availability_logistics"] == 1.0
        assert _attributes["availability_mission"] == 1.0
        assert _attributes["cost"] == 0.0
        assert _attributes["function_code"] == "PRESS-001"
        assert _attributes["hazard_rate_logistics"] == 0.0
        assert _attributes["hazard_rate_mission"] == 0.0
        assert _attributes["level"] == 0
        assert _attributes["mmt"] == 0.0
        assert _attributes["mcmt"] == 0.0
        assert _attributes["mpmt"] == 0.0
        assert _attributes["mtbf_logistics"] == 0.0
        assert _attributes["mtbf_mission"] == 0.0
        assert _attributes["mttr"] == 0.0
        assert _attributes["name"] == "Function Name"
        assert _attributes["parent_id"] == 0
        assert _attributes["remarks"] == ""
        assert _attributes["safety_critical"] == 0
        assert _attributes["total_mode_count"] == 0
        assert _attributes["total_part_count"] == 0
        assert _attributes["type_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["safety_critical"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["safety_critical"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
