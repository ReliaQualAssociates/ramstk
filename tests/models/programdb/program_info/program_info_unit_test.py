# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.preferences.preferences_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Preferences module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramInfoRecord
from ramstk.models.dbtables import RAMSTKProgramInfoTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramInfoTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_preference_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_preference_attributes")
    pub.unsubscribe(dut.do_update, "request_update_preference")
    pub.unsubscribe(dut.do_get_tree, "request_get_preference_tree")
    pub.unsubscribe(dut.do_select_all, "request_program_preferences")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKProgramInfoRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_program_info"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.function_active == 1
        assert test_recordmodel.requirement_active == 1
        assert test_recordmodel.hardware_active == 1
        assert test_recordmodel.software_active == 0
        assert test_recordmodel.rcm_active == 0
        assert test_recordmodel.testing_active == 0
        assert test_recordmodel.incident_active == 0
        assert test_recordmodel.survival_active == 0
        assert test_recordmodel.vandv_active == 1
        assert test_recordmodel.hazard_active == 1
        assert test_recordmodel.stakeholder_active == 1
        assert test_recordmodel.allocation_active == 1
        assert test_recordmodel.similar_item_active == 1
        assert test_recordmodel.fmea_active == 1
        assert test_recordmodel.pof_active == 1
        assert test_recordmodel.rbd_active == 0
        assert test_recordmodel.fta_active == 0
        assert test_recordmodel.created_on == date.today()
        assert test_recordmodel.created_by == ""
        assert test_recordmodel.last_saved == date.today()
        assert test_recordmodel.last_saved_by == ""

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a Options data manager."""
        assert isinstance(test_tablemodel, RAMSTKProgramInfoTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._tag == "preference"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(
            test_tablemodel.do_select_all, "request_program_preferences"
        )
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_preference")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_preference_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_preference_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_preference_attributes"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["preference"], RAMSTKProgramInfoRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKProgramInfo on
        success."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        _record = test_tablemodel.do_select(1)

        assert isinstance(_record, RAMSTKProgramInfoRecord)
        assert _record.function_active == 1
        assert _record.requirement_active == 1
        assert _record.hardware_active == 1
        assert _record.software_active == 0
        assert _record.rcm_active == 0
        assert _record.testing_active == 0
        assert _record.incident_active == 0
        assert _record.survival_active == 0
        assert _record.vandv_active == 1
        assert _record.hazard_active == 1
        assert _record.stakeholder_active == 1
        assert _record.allocation_active == 1
        assert _record.similar_item_active == 1
        assert _record.fmea_active == 1
        assert _record.pof_active == 1
        assert _record.rbd_active == 0
        assert _record.fta_active == 0
        assert _record.created_on == date.today()
        assert _record.created_by == ""
        assert _record.last_saved == date.today()
        assert _record.last_saved_by == ""

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["function_active"] == 1
        assert _attributes["requirement_active"] == 1
        assert _attributes["hardware_active"] == 1
        assert _attributes["software_active"] == 0
        assert _attributes["rcm_active"] == 0
        assert _attributes["testing_active"] == 0
        assert _attributes["incident_active"] == 0
        assert _attributes["survival_active"] == 0
        assert _attributes["vandv_active"] == 1
        assert _attributes["hazard_active"] == 1
        assert _attributes["stakeholder_active"] == 1
        assert _attributes["allocation_active"] == 1
        assert _attributes["similar_item_active"] == 1
        assert _attributes["fmea_active"] == 1
        assert _attributes["pof_active"] == 1
        assert _attributes["rbd_active"] == 0
        assert _attributes["fta_active"] == 0
        assert _attributes["created_on"] == date.today()
        assert _attributes["created_by"] == ""
        assert _attributes["last_saved"] == date.today()
        assert _attributes["last_saved_by"] == ""

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
        test_attributes["created_on"] = None

        test_attributes.pop("revision_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["created_on"] == date.today()

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
