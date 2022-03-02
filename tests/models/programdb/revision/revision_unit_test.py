# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRevisionRecord
from ramstk.models.dbtables import RAMSTKRevisionTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Test fixture for Function data manager."""
    dut = RAMSTKRevisionTable()
    dut.do_connect(mock_program_dao)
    dut.do_select_all(
        attributes={
            None: None,
        }
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_revision")
    pub.unsubscribe(dut.do_update, "request_update_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_revision_tree")
    pub.unsubscribe(dut.do_select_all, "request_retrieve_revisions")
    pub.unsubscribe(dut.do_delete, "request_delete_revision")
    pub.unsubscribe(dut.do_insert, "request_insert_revision")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKRevisionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_revision"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.availability_logistics == 0.9986
        assert test_recordmodel.availability_mission == 0.99934
        assert test_recordmodel.cost == 12532.15
        assert test_recordmodel.cost_failure == 3.52e-05
        assert test_recordmodel.cost_hour == 1.2532
        assert test_recordmodel.hazard_rate_active == 0.0
        assert test_recordmodel.hazard_rate_dormant == 0.0
        assert test_recordmodel.hazard_rate_logistics == 0.0
        assert test_recordmodel.hazard_rate_mission == 0.0
        assert test_recordmodel.hazard_rate_software == 0.0
        assert test_recordmodel.mmt == 0.0
        assert test_recordmodel.mcmt == 0.0
        assert test_recordmodel.mpmt == 0.0
        assert test_recordmodel.mtbf_logistics == 0.0
        assert test_recordmodel.mtbf_mission == 0.0
        assert test_recordmodel.mttr == 0.0
        assert test_recordmodel.name == "Original Revision"
        assert test_recordmodel.reliability_logistics == 0.99986
        assert test_recordmodel.reliability_mission == 0.99992
        assert test_recordmodel.remarks == "This is the original revision."
        assert test_recordmodel.revision_code == "Rev. -"
        assert test_recordmodel.program_time == 2562
        assert test_recordmodel.program_time_sd == 26.83
        assert test_recordmodel.program_cost == 26492.83
        assert test_recordmodel.program_cost_sd == 15.62

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKRevisionTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_revision_id"
        assert test_tablemodel._db_tablename == "ramstk_revision"
        assert test_tablemodel._tag == "revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKRevisionRecord
        assert pub.isSubscribed(
            test_tablemodel.do_select_all, "request_retrieve_revisions"
        )
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_revisions"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_revision_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_revision_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_revision_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_revision")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_revision")


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """should return a record tree populated with DB records."""
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["revision"], RAMSTKRevisionRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """should return the record for the passed record ID."""
        _revision = test_tablemodel.do_select(1)

        assert isinstance(_revision, RAMSTKRevisionRecord)
        assert _revision.availability_logistics == 0.9986
        assert _revision.name == "Original Revision"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKRevisionRecord)
        assert _new_record.revision_id == 3

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.last_id == 2

        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["revision"], RAMSTKRevisionRecord
        )
        assert test_tablemodel.tree.get_node(3).data["revision"].revision_id == 3
        assert (
            test_tablemodel.tree.get_node(3).data["revision"].name
            == "Original Revision"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_delete(2)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["availability_logistics"] == 0.9986
        assert _attributes["availability_mission"] == 0.99934
        assert _attributes["cost"] == 12532.15
        assert _attributes["cost_failure"] == 3.52e-05
        assert _attributes["cost_hour"] == 1.2532
        assert _attributes["hazard_rate_active"] == 0.0
        assert _attributes["hazard_rate_dormant"] == 0.0
        assert _attributes["hazard_rate_logistics"] == 0.0
        assert _attributes["hazard_rate_mission"] == 0.0
        assert _attributes["hazard_rate_software"] == 0.0
        assert _attributes["mmt"] == 0.0
        assert _attributes["mcmt"] == 0.0
        assert _attributes["mpmt"] == 0.0
        assert _attributes["mtbf_logistics"] == 0.0
        assert _attributes["mtbf_mission"] == 0.0
        assert _attributes["mttr"] == 0.0
        assert _attributes["name"] == "Original Revision"
        assert _attributes["reliability_logistics"] == 0.99986
        assert _attributes["reliability_mission"] == 0.99992
        assert _attributes["remarks"] == "This is the original revision."
        assert _attributes["revision_code"] == "Rev. -"
        assert _attributes["program_time"] == 2562
        assert _attributes["program_time_sd"] == 26.83
        assert _attributes["program_cost"] == 26492.83
        assert _attributes["program_cost_sd"] == 15.62

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["mtbf_mission"] = None

        test_attributes.pop("revision_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["mtbf_mission"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
