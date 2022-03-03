# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.cause.cause_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord
from ramstk.models.dbtables import RAMSTKCauseTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCauseTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_cause")
    pub.unsubscribe(dut.do_insert, "request_insert_cause")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_cause_rpn")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKCauseRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_cause"
        assert (
            test_recordmodel.description == "Test Failure Cause #1 for Mechanism ID 3"
        )
        assert test_recordmodel.rpn == 0
        assert test_recordmodel.rpn_new == 0
        assert test_recordmodel.rpn_detection == 3
        assert test_recordmodel.rpn_detection_new == 3
        assert test_recordmodel.rpn_occurrence_new == 6
        assert test_recordmodel.rpn_occurrence == 4

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_tablemodel, RAMSTKCauseTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_cause_id"
        assert test_tablemodel._db_tablename == "ramstk_cause"
        assert test_tablemodel._tag == "cause"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_cause_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_cause_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_set_attributes, "wvw_editing_cause")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_cause")
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_cause_tree")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_cause")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_cause")
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_rpn, "request_calculate_cause_rpn"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """should return a Tree() object populated with RAMSTKCauseRecord instances."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["cause"], RAMSTKCauseRecord
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["cause"], RAMSTKCauseRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKCauseRecord on
        success."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        _cause = test_tablemodel.do_select(1)

        assert isinstance(_cause, RAMSTKCauseRecord)
        assert _cause.description == "Test Failure Cause #1 for Mechanism ID 3"
        assert _cause.rpn == 0
        assert _cause.rpn_new == 0
        assert _cause.rpn_detection == 3
        assert _cause.rpn_detection_new == 3
        assert _cause.rpn_occurrence_new == 6
        assert _cause.rpn_occurrence == 4

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent cause ID is requested."""
        test_tablemodel.do_select_all(
            {
                "revision_id": 1,
            }
        )

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        test_tablemodel.do_select_all(test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["cause"], RAMSTKCauseRecord
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(test_attributes)
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
        assert _attributes["description"] == "Test Failure Cause #1 for Mechanism ID 3"
        assert _attributes["rpn"] == 0
        assert _attributes["rpn_detection"] == 3
        assert _attributes["rpn_detection_new"] == 3
        assert _attributes["rpn_new"] == 0
        assert _attributes["rpn_occurrence"] == 4
        assert _attributes["rpn_occurrence_new"] == 6

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["rpn_detection_new"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["rpn_detection_new"] == 10

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
        test_attributes.pop("cause_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, test_tablemodel):
        """should calculate the cause RPN."""
        test_tablemodel.do_select_all(test_attributes)

        test_tablemodel.tree.get_node(1).data["cause"].rpn_occurrence = 8
        test_tablemodel.tree.get_node(1).data["cause"].rpn_detection = 3
        test_tablemodel.tree.get_node(2).data["cause"].rpn_occurrence = 4
        test_tablemodel.tree.get_node(2).data["cause"].rpn_detection = 5

        test_tablemodel.do_calculate_rpn(8)

        assert test_tablemodel.tree.get_node(1).data["cause"].rpn == 192
        assert test_tablemodel.tree.get_node(2).data["cause"].rpn == 160
