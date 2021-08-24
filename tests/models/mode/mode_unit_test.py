# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.mode.mode_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure mode algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKModeRecord, RAMSTKModeTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKModeTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mode")
    pub.unsubscribe(dut.do_insert, "request_insert_mode")
    pub.unsubscribe(dut.do_calculate_criticality, "request_calculate_criticality")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKModeRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_mode"
        assert test_recordmodel.effect_local == ""
        assert test_recordmodel.mission == "Default Mission"
        assert test_recordmodel.other_indications == ""
        assert test_recordmodel.mode_criticality == 0.0
        assert test_recordmodel.single_point == 0
        assert test_recordmodel.design_provisions == ""
        assert test_recordmodel.type_id == 0
        assert test_recordmodel.rpn_severity_new == 1
        assert test_recordmodel.effect_next == ""
        assert test_recordmodel.detection_method == ""
        assert test_recordmodel.operator_actions == ""
        assert test_recordmodel.critical_item == 0
        assert test_recordmodel.hazard_rate_source == ""
        assert test_recordmodel.severity_class == ""
        assert test_recordmodel.description == "Test Failure Mode #1"
        assert test_recordmodel.mission_phase == ""
        assert test_recordmodel.mode_probability == ""
        assert test_recordmodel.remarks == ""
        assert test_recordmodel.mode_ratio == 0.0
        assert test_recordmodel.mode_hazard_rate == 0.0
        assert test_recordmodel.rpn_severity == 1
        assert test_recordmodel.isolation_method == ""
        assert test_recordmodel.effect_end == ""
        assert test_recordmodel.mode_op_time == 0.0
        assert test_recordmodel.effect_probability == 0.8

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKModeTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_mode_id"
        assert test_tablemodel._db_tablename == "ramstk_mode"
        assert test_tablemodel._tag == "mode"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_mode_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_mode_tree")
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_mode")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_mode"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_mode")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_mode")
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_criticality, "request_calculate_criticality"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["mode"], RAMSTKModeRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _mode = test_tablemodel.do_select(1)

        assert isinstance(_mode, RAMSTKModeRecord)
        assert _mode.effect_probability == 0.8
        assert _mode.description == "Test Failure Mode #1"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """should return None when a non-existent record ID is requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_tablemodel):
        """should return a new record instance with ID fields populated."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKModeRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["mode"], RAMSTKModeRecord
        )
        assert test_tablemodel.tree.get_node(3).data["mode"].mode_id == 3
        assert test_tablemodel.tree.get_node(3).data["mode"].description == ""


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_delete(4)

        assert test_tablemodel.tree.get_node(4) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["critical_item"] == 0
        assert _attributes["description"] == "Test Failure Mode #1"
        assert _attributes["design_provisions"] == ""
        assert _attributes["detection_method"] == ""
        assert _attributes["effect_end"] == ""
        assert _attributes["effect_local"] == ""
        assert _attributes["effect_next"] == ""
        assert _attributes["effect_probability"] == 0.8
        assert _attributes["hazard_rate_source"] == ""
        assert _attributes["isolation_method"] == ""
        assert _attributes["mission"] == "Default Mission"
        assert _attributes["mission_phase"] == ""
        assert _attributes["mode_criticality"] == 0.0
        assert _attributes["mode_hazard_rate"] == 0.0
        assert _attributes["mode_op_time"] == 0.0
        assert _attributes["mode_probability"] == ""
        assert _attributes["mode_ratio"] == 0.0
        assert _attributes["operator_actions"] == ""
        assert _attributes["other_indications"] == ""
        assert _attributes["remarks"] == ""
        assert _attributes["rpn_severity"] == 1
        assert _attributes["rpn_severity_new"] == 1
        assert _attributes["severity_class"] == ""
        assert _attributes["single_point"] == 0
        assert _attributes["type_id"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["mode_ratio"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["mode_ratio"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for analytical method tests."""

    @pytest.mark.unit
    def test_do_calculate_criticality(self, test_attributes, test_tablemodel):
        """should calculate the mode hazard rate and mode criticality."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        test_tablemodel.tree.get_node(1).data["mode"].mode_ratio = 0.428
        test_tablemodel.tree.get_node(1).data["mode"].mode_op_time = 4.2
        test_tablemodel.tree.get_node(1).data["mode"].effect_probability = 1.0
        test_tablemodel.tree.get_node(1).data["mode"].severity_class = "III"

        test_tablemodel.do_calculate_criticality(0.00000682)

        assert test_tablemodel.tree.get_node(1).data[
            "mode"
        ].mode_hazard_rate == pytest.approx(2.91896e-06)
        assert test_tablemodel.tree.get_node(1).data[
            "mode"
        ].mode_criticality == pytest.approx(1.2259632e-05)
