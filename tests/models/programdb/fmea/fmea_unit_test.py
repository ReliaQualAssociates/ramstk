# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.fmea.fmea_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.models import RAMSTKFMEARecord, RAMSTKFMEAView


@pytest.fixture(scope="function")
def test_viewmodel():
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFMEAView()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_insert_action")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_modes")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_mechanisms")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_causes")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_controls")
    pub.unsubscribe(dut.do_set_tree, "succeed_retrieve_actions")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mode")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_mechanism")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_cause")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_control")
    pub.unsubscribe(dut.do_set_tree, "succeed_delete_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_viewmodel")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKFMEARecord)
        assert test_recordmodel.__tablename__ == "ramstk_fmeca"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.hardware_id == 1
        assert test_recordmodel.mode_id == 6
        assert test_recordmodel.mechanism_id == 3
        assert test_recordmodel.cause_id == 3
        assert test_recordmodel.control_id == 1
        assert test_recordmodel.action_id == 1
        assert (
            test_recordmodel.mode_description == "Test FMEA Mode #6 for Hardware ID #1."
        )
        assert (
            test_recordmodel.mechanism_description
            == "Test FMEA Mechanism #3 for Mode ID #6."
        )
        assert (
            test_recordmodel.cause_description
            == "Test FMEA Cause #3 for Mechanism ID #3."
        )
        assert (
            test_recordmodel.control_description
            == "Test FMEA Control #1 for Cause ID #3."
        )
        assert (
            test_recordmodel.action_description
            == "Test FMEA Action #1 for Cause ID #3."
        )
        assert test_recordmodel.mission == "Big Mission"
        assert test_recordmodel.mission_phase == "Phase 1"
        assert test_recordmodel.effect_local == "Local Effect"
        assert test_recordmodel.effect_next == "Next Effect"
        assert test_recordmodel.effect_end == "End Effect"
        assert test_recordmodel.detection_method == "Detection Method"
        assert test_recordmodel.other_indications == "Other Indications"
        assert test_recordmodel.isolation_method == "Isolation Method"
        assert test_recordmodel.design_provisions == "Design Provisions"
        assert test_recordmodel.operator_actions == "Operations Actions"
        assert test_recordmodel.severity_class == "III"
        assert test_recordmodel.hazard_rate_source == "MIL-HDBK-217FN2"
        assert test_recordmodel.mode_probability == "Maybe?"
        assert test_recordmodel.effect_probability == 1.0
        assert test_recordmodel.hazard_rate_active == 0.000035
        assert test_recordmodel.mode_ratio == 0.5
        assert test_recordmodel.mode_hazard_rate == 0.0
        assert test_recordmodel.mode_op_time == 1.0
        assert test_recordmodel.mode_criticality == 0.5
        assert test_recordmodel.type_id == 1
        assert test_recordmodel.rpn_severity == 5
        assert test_recordmodel.rpn_occurrence == 6
        assert test_recordmodel.rpn_detection == 3
        assert test_recordmodel.rpn == 90
        assert test_recordmodel.action_category == ""
        assert test_recordmodel.action_owner == "weibullguy"
        assert test_recordmodel.action_due_date == date.today()
        assert test_recordmodel.action_status == "Closed"
        assert test_recordmodel.action_taken == "Basically just screwed around"
        assert test_recordmodel.action_approved == 1
        assert test_recordmodel.action_approve_date == date.today()
        assert test_recordmodel.action_closed == 1
        assert test_recordmodel.action_close_date == date.today()
        assert test_recordmodel.rpn_severity_new == 5
        assert test_recordmodel.rpn_occurrence_new == 3
        assert test_recordmodel.rpn_detection_new == 3
        assert test_recordmodel.rpn_new == 45
        assert test_recordmodel.single_point == 1
        assert test_recordmodel.pof_include == 1
        assert test_recordmodel.remarks == "Say something about this failure mode."
        assert test_recordmodel.hardware_description == "Capacitor Ceramic 10uF"

    @pytest.mark.skip
    def test_data_manager_create(self, test_viewmodel):
        """should return a view manager instance."""
        assert isinstance(test_viewmodel, RAMSTKFMEAView)
        assert isinstance(test_viewmodel.tree, Tree)
        assert isinstance(test_viewmodel.dao, BaseDatabase)
        assert test_viewmodel._tag == "fmea"
        assert test_viewmodel._root == 0
        assert test_viewmodel._revision_id == 0
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_mode")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_mechanism")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_cause")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_control")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_insert_action")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_modes")
        assert pub.isSubscribed(
            test_viewmodel.do_set_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_causes")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_controls")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_retrieve_actions")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mode")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_cause")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_control")
        assert pub.isSubscribed(test_viewmodel.do_set_tree, "succeed_delete_action")


@pytest.mark.usefixtures("test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["hardware_id"] == 1
        assert _attributes["mode_id"] == 6
        assert _attributes["mechanism_id"] == 3
        assert _attributes["cause_id"] == 3
        assert _attributes["control_id"] == 1
        assert _attributes["action_id"] == 1
        assert (
            _attributes["mode_description"] == "Test FMEA Mode #6 for Hardware ID #1."
        )
        assert (
            _attributes["mechanism_description"]
            == "Test FMEA Mechanism #3 for Mode ID #6."
        )
        assert (
            _attributes["cause_description"]
            == "Test FMEA Cause #3 for Mechanism ID #3."
        )
        assert (
            _attributes["control_description"]
            == "Test FMEA Control #1 for Cause ID #3."
        )
        assert (
            _attributes["action_description"] == "Test FMEA Action #1 for Cause ID #3."
        )
        assert _attributes["mission"] == "Big Mission"
        assert _attributes["mission_phase"] == "Phase 1"
        assert _attributes["effect_local"] == "Local Effect"
        assert _attributes["effect_next"] == "Next Effect"
        assert _attributes["effect_end"] == "End Effect"
        assert _attributes["detection_method"] == "Detection Method"
        assert _attributes["other_indications"] == "Other Indications"
        assert _attributes["isolation_method"] == "Isolation Method"
        assert _attributes["design_provisions"] == "Design Provisions"
        assert _attributes["operator_actions"] == "Operations Actions"
        assert _attributes["severity_class"] == "III"
        assert _attributes["hazard_rate_source"] == "MIL-HDBK-217FN2"
        assert _attributes["mode_probability"] == "Maybe?"
        assert _attributes["effect_probability"] == 1.0
        assert _attributes["hazard_rate_active"] == 0.000035
        assert _attributes["mode_ratio"] == 0.5
        assert _attributes["mode_hazard_rate"] == 0.0
        assert _attributes["mode_op_time"] == 1.0
        assert _attributes["mode_criticality"] == 0.5
        assert _attributes["type_id"] == 1
        assert _attributes["rpn_severity"] == 5
        assert _attributes["rpn_occurrence"] == 6
        assert _attributes["rpn_detection"] == 3
        assert _attributes["rpn"] == 90
        assert _attributes["action_category"] == ""
        assert _attributes["action_owner"] == "weibullguy"
        assert _attributes["action_due_date"] == date.today()
        assert _attributes["action_status"] == "Closed"
        assert _attributes["action_taken"] == "Basically just screwed around"
        assert _attributes["action_approved"] == 1
        assert _attributes["action_approve_date"] == date.today()
        assert _attributes["action_closed"] == 1
        assert _attributes["action_close_date"] == date.today()
        assert _attributes["rpn_severity_new"] == 5
        assert _attributes["rpn_occurrence_new"] == 3
        assert _attributes["rpn_detection_new"] == 3
        assert _attributes["rpn_new"] == 45
        assert _attributes["single_point"] == 1
        assert _attributes["pof_include"] == 1
        assert _attributes["remarks"] == "Say something about this failure mode."
        assert _attributes["hardware_description"] == "Capacitor Ceramic 10uF"
