# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.environment.environment_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKEnvironmentRecord, RAMSTKEnvironmentTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKEnvironmentTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKEnvironmentRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_environment"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.name == "Condition Name"
        assert test_recordmodel.units == "Units"
        assert test_recordmodel.minimum == 0.0
        assert test_recordmodel.maximum == 0.0
        assert test_recordmodel.mean == 0.0
        assert test_recordmodel.variance == 0.0
        assert test_recordmodel.ramp_rate == 0.0
        assert test_recordmodel.low_dwell_time == 0.0
        assert test_recordmodel.high_dwell_time == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return an Environment data manager."""
        assert isinstance(test_tablemodel, RAMSTKEnvironmentTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert test_tablemodel._db_id_colname == "fld_environment_id"
        assert test_tablemodel._db_tablename == "ramstk_environment"
        assert test_tablemodel._tag == "environment"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_environment_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_environment_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_environment")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_environments"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_environment")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_environment")


@pytest.mark.usefixtures("test_tablemodel", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with RAMSTKMission,
        RAMSTKMissionPhase, and RAMSTKEnvironmentRecord instances on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["environment"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["environment"],
            RAMSTKEnvironmentRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["environment"],
            RAMSTKEnvironmentRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return the RAMSTKEnvironmentRecord instance on
        success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _environment = test_tablemodel.do_select(1)

        assert isinstance(_environment, RAMSTKEnvironmentRecord)
        assert _environment.environment_id == 1

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add the new record to the record tree and update the last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["environment"],
            RAMSTKEnvironmentRecord,
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the deleted record from record tree and update the last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(_last_id)

        assert test_tablemodel.last_id == 2
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["name"] == "Condition Name"
        assert _attributes["units"] == "Units"
        assert _attributes["minimum"] == 0.0
        assert _attributes["maximum"] == 0.0
        assert _attributes["mean"] == 0.0
        assert _attributes["variance"] == 0.0
        assert _attributes["ramp_rate"] == 0.0
        assert _attributes["low_dwell_time"] == 0.0
        assert _attributes["high_dwell_time"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("environment_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["minimum"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("environment_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["minimum"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("environment_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
