# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMechanismRecord
from ramstk.models.dbtables import RAMSTKMechanismTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMechanismTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut.do_insert, "request_insert_mechanism")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_mechanism_rpn")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKMechanismRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_mechanism"
        assert test_recordmodel.description == "Test Failure Mechanism #1"
        assert test_recordmodel.rpn == 100
        assert test_recordmodel.rpn_new == 100
        assert test_recordmodel.rpn_detection == 10
        assert test_recordmodel.rpn_detection_new == 10
        assert test_recordmodel.rpn_occurrence_new == 10
        assert test_recordmodel.rpn_occurrence == 10
        assert test_recordmodel.pof_include == 1

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_tablemodel, RAMSTKMechanismTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_mechanism_id"
        assert test_tablemodel._db_tablename == "ramstk_mechanism"
        assert test_tablemodel._tag == "mechanism"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._parent_id == 0
        assert test_tablemodel.last_id == 0
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_mechanism_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_mechanism_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_mechanism"
        )
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_mechanism")
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_mechanism_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_mechanism")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_mechanism")
        assert pub.isSubscribed(
            test_tablemodel.do_calculate_rpn, "request_calculate_mechanism_rpn"
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMechanismRecord instances on success."""
        test_tablemodel.do_select_all(test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["mechanism"], RAMSTKMechanismRecord
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["mechanism"], RAMSTKMechanismRecord
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return an instance of the RAMSTKMechanismRecord on
        success."""
        test_tablemodel.do_select_all(test_attributes)

        _mechanism = test_tablemodel.do_select(1)

        assert isinstance(_mechanism, RAMSTKMechanismRecord)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 10

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent mechanism ID is
        requested."""
        test_tablemodel.do_select_all(test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        test_tablemodel.do_select_all(test_attributes)

        assert test_tablemodel.tree.get_node(3) is None

        test_tablemodel.do_insert(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(3).data["mechanism"], RAMSTKMechanismRecord
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(test_attributes)
        test_tablemodel.do_delete(2)

        assert test_tablemodel.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test Failure Mechanism #1"
        assert _attributes["pof_include"] == 1
        assert _attributes["rpn"] == 100
        assert _attributes["rpn_detection"] == 10
        assert _attributes["rpn_detection_new"] == 10
        assert _attributes["rpn_new"] == 100
        assert _attributes["rpn_occurrence"] == 10
        assert _attributes["rpn_occurrence_new"] == 10

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        test_attributes.pop("mode_id")
        test_attributes.pop("mechanism_id")
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
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, test_tablemodel):
        """should calculate the mechanism RPN."""
        test_tablemodel.do_select_all(test_attributes)

        test_tablemodel.tree.get_node(1).data["mechanism"].rpn_occurrence = 8
        test_tablemodel.tree.get_node(1).data["mechanism"].rpn_detection = 3
        test_tablemodel.tree.get_node(2).data["mechanism"].rpn_occurrence = 4
        test_tablemodel.tree.get_node(2).data["mechanism"].rpn_detection = 5

        test_tablemodel.do_calculate_rpn(8)

        assert test_tablemodel.tree.get_node(1).data["mechanism"].rpn == 192
        assert test_tablemodel.tree.get_node(2).data["mechanism"].rpn == 160
