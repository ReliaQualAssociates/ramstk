# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission.mission_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMissionRecord, RAMSTKMissionTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKMissionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_mission"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.description == "Test mission #1"
        assert test_recordmodel.mission_time == 100.0
        assert test_recordmodel.time_units == "hours"

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return an Mission data manager."""
        assert isinstance(test_tablemodel, RAMSTKMissionTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_mission_id"
        assert test_tablemodel._db_tablename == "ramstk_mission"
        assert test_tablemodel._tag == "mission"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_mission_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_mission_tree")
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_mission")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_mission"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_mission")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_mission")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["mission"], RAMSTKMissionRecord
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["mission"], RAMSTKMissionRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return the RAMSTKMission instance on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _mission = test_tablemodel.do_select(1)

        assert isinstance(_mission, RAMSTKMissionRecord)
        assert _mission.mission_id == 1

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
        """do_insert() should send the success message after successfully inserting a
        new mission."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["mission"], RAMSTKMissionRecord
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """_do_delete_mission() should send the success message after successfully
        deleting a mission."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(1)

        assert test_tablemodel.tree.get_node(1) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["description"] == "Test mission #1"
        assert _attributes["mission_time"] == 100.0
        assert _attributes["time_units"] == "hours"

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["mission_time"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["mission_time"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
