# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission_phase.mission_phase_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission Phase module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMissionPhaseRecord, RAMSTKMissionPhaseTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMissionPhaseTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut.do_insert, "request_insert_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKMissionPhaseRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_mission_phase"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.description == "Phase #1 for mission #1"
        assert test_recordmodel.name == "Start Up"
        assert test_recordmodel.phase_start == 0.0
        assert test_recordmodel.phase_end == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKMissionPhaseTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_mission_phase_id"
        assert test_tablemodel._db_tablename == "ramstk_mission_phase"
        assert test_tablemodel._tag == "mission_phase"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_mission_phase_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_mission_phase_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update, "request_update_mission_phase"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_mission_phases"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_delete, "request_delete_mission_phase"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_insert, "request_insert_mission_phase"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMissionPhaseRecord instances on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["mission_phase"],
            RAMSTKMissionPhaseRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["mission_phase"],
            RAMSTKMissionPhaseRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return the RAMSTKMission instance on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _mission_phase = test_tablemodel.do_select(1)

        assert isinstance(_mission_phase, RAMSTKMissionPhaseRecord)
        assert _mission_phase.mission_phase_id == 1

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
            test_tablemodel.tree.get_node(4).data["mission_phase"],
            RAMSTKMissionPhaseRecord,
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """_do_delete() should remove the passed mission phase ID."""
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
        assert _attributes["mission_phase_id"] == 1
        assert _attributes["description"] == "Phase #1 for mission #1"
        assert _attributes["name"] == "Start Up"
        assert _attributes["phase_start"] == 0.0
        assert _attributes["phase_end"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["phase_start"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["phase_start"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("mission_id")
        test_attributes.pop("mission_phase_id")
        test_attributes.pop("parent_id")
        test_attributes.pop("record_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
