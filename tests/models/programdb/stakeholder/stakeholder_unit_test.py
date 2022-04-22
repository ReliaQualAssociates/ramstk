# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.stakeholder.stakeholder_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholderRecord
from ramstk.models.dbtables import RAMSTKStakeholderTable

# noinspection PyUnresolvedReferences
from tests import MockDAO


@pytest.fixture(scope="function")
def test_tablemodel(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStakeholderTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholder")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut.do_insert, "request_insert_stakeholder")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKStakeholderRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_stakeholder"
        assert test_record_model.revision_id == 1
        assert test_record_model.customer_rank == 1
        assert test_record_model.description == "Stakeholder Input"
        assert test_record_model.group == ""
        assert test_record_model.improvement == 0.0
        assert test_record_model.overall_weight == 0.0
        assert test_record_model.planned_rank == 1
        assert test_record_model.priority == 1
        assert test_record_model.stakeholder == ""
        assert test_record_model.user_float_1 == 1.0
        assert test_record_model.user_float_2 == 1.0
        assert test_record_model.user_float_3 == 1.0
        assert test_record_model.user_float_4 == 1.0
        assert test_record_model.user_float_5 == 1.0

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKStakeholderTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert test_tablemodel._db_id_colname == "fld_stakeholder_id"
        assert test_tablemodel._db_tablename == "ramstk_stakeholder"
        assert test_tablemodel._tag == "stakeholder"
        assert test_tablemodel._root == 0
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "stakeholder_id",
            "parent_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKStakeholderRecord
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "stakeholder_id"
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_stakeholder")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_stakeholder"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_stakeholder_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_stakeholder_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_stakeholder_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_stakeholder")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_stakeholder")
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_stakeholder, "request_calculate_stakeholder"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.tree.get_node(1).data, dict)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["stakeholder"],
            RAMSTKStakeholderRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _stakeholder = test_tablemodel.do_select(1)

        assert isinstance(_stakeholder, RAMSTKStakeholderRecord)
        assert _stakeholder.description == "Stakeholder Input"
        assert _stakeholder.priority == 1

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
        test_attributes["parent_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        _new_record = test_tablemodel.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKStakeholderRecord)
        assert _new_record.revision_id == 1
        assert _new_record.stakeholder_id == 3

    @pytest.mark.unit
    def test_do_insert(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_attributes["parent_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["stakeholder"],
            RAMSTKStakeholderRecord,
        )
        assert test_tablemodel.tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert (
            test_tablemodel.tree.get_node(3).data["stakeholder"].description
            == "Stakeholder Input"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_attributes["parent_id"] = 1
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(test_tablemodel.last_id)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["customer_rank"] == 1
        assert _attributes["description"] == "Stakeholder Input"
        assert _attributes["group"] == ""
        assert _attributes["improvement"] == 0.0
        assert _attributes["overall_weight"] == 0.0
        assert _attributes["planned_rank"] == 1
        assert _attributes["priority"] == 1
        assert _attributes["requirement_id"] == 1
        assert _attributes["stakeholder"] == ""
        assert _attributes["user_float_1"] == 1.0
        assert _attributes["user_float_2"] == 1.0
        assert _attributes["user_float_3"] == 1.0
        assert _attributes["user_float_4"] == 1.0
        assert _attributes["user_float_5"] == 1.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_record_model):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        test_attributes.pop("stakeholder_id")
        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_record_model
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["overall_weight"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        test_attributes.pop("stakeholder_id")
        assert test_record_model.set_attributes(test_attributes) is None
        assert test_record_model.get_attributes()["overall_weight"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_record_model
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("requirement_id")
        test_attributes.pop("stakeholder_id")
        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_improvement(self, test_attributes, test_tablemodel):
        """should calculate the record's improvement factor and overall weight."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _stakeholder = test_tablemodel.do_select(1)
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        test_tablemodel.do_update(1)

        test_tablemodel._do_calculate_improvement(1)
        _attributes = test_tablemodel.do_select(1).get_attributes()

        assert _attributes["improvement"] == 1.2
        assert _attributes["overall_weight"] == 12.48
