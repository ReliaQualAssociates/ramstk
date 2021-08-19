# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.milhdbk217f.milhdbk217f_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing MIL-HDBK-217F module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMilHdbk217FRecord, RAMSTKMILHDBK217FTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_milhdbk217f")
    pub.unsubscribe(dut.do_update, "request_update_milhdbk217f")
    pub.unsubscribe(dut.do_get_tree, "request_get_milhdbk217f_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_milhdbk217f")
    pub.unsubscribe(dut.do_insert, "request_insert_milhdbk217f")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_ramstkmilhdbkf_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKMilHdbk217FRecord)
        assert test_recordmodel.__tablename__ == "ramstk_mil_hdbk_f"
        assert test_recordmodel.hardware_id == 1
        assert test_recordmodel.A1 == 0.0
        assert test_recordmodel.A2 == 0.0
        assert test_recordmodel.B1 == 0.0
        assert test_recordmodel.B2 == 0.0
        assert test_recordmodel.C1 == 0.0
        assert test_recordmodel.C2 == 0.0
        assert test_recordmodel.lambdaBD == 0.0
        assert test_recordmodel.lambdaBP == 0.0
        assert test_recordmodel.lambdaCYC == 0.0
        assert test_recordmodel.lambdaEOS == 0.0
        assert test_recordmodel.piA == 0.0
        assert test_recordmodel.piC == 0.0
        assert test_recordmodel.piCD == 0.0
        assert test_recordmodel.piCF == 0.0
        assert test_recordmodel.piCR == 0.0
        assert test_recordmodel.piCV == 0.0
        assert test_recordmodel.piCYC == 0.0
        assert test_recordmodel.piE == 0.0
        assert test_recordmodel.piF == 0.0
        assert test_recordmodel.piI == 0.0
        assert test_recordmodel.piK == 0.0
        assert test_recordmodel.piL == 0.0
        assert test_recordmodel.piM == 0.0
        assert test_recordmodel.piMFG == 0.0
        assert test_recordmodel.piN == 0.0
        assert test_recordmodel.piNR == 0.0
        assert test_recordmodel.piP == 0.0
        assert test_recordmodel.piPT == 0.0
        assert test_recordmodel.piQ == 0.0
        assert test_recordmodel.piR == 0.0
        assert test_recordmodel.piS == 0.0
        assert test_recordmodel.piT == 0.0
        assert test_recordmodel.piTAPS == 0.0
        assert test_recordmodel.piU == 0.0
        assert test_recordmodel.piV == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table model instance."""
        assert isinstance(test_tablemodel, RAMSTKMILHDBK217FTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_mil_hdbk_f"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "milhdbk217f"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKMilHdbk217FRecord
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_milhdbk217f_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_milhdbk217f_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_milhdbk217f"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_milhdbk217f"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_milhdbk217f_tree"
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_milhdbk217f")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_milhdbk217f")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_milhdbk217f")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _milhdbk217f = test_tablemodel.do_select(1)

        assert isinstance(_milhdbk217f, RAMSTKMilHdbk217FRecord)
        assert _milhdbk217f.revision_id == 1
        assert _milhdbk217f.hardware_id == 1
        assert _milhdbk217f.lambdaBD == 0.0

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

        assert isinstance(_new_record, RAMSTKMilHdbk217FRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert test_tablemodel.tree.get_node(4).data["milhdbk217f"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["milhdbk217f"].hardware_id == 4


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove the record from the record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(node_id=_last_id)

        assert test_tablemodel.last_id == 2
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel", "mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["A1"] == 0.0
        assert _attributes["A2"] == 0.0
        assert _attributes["B1"] == 0.0
        assert _attributes["B2"] == 0.0
        assert _attributes["C1"] == 0.0
        assert _attributes["C2"] == 0.0
        assert _attributes["lambdaBD"] == 0.0
        assert _attributes["lambdaBP"] == 0.0
        assert _attributes["lambdaCYC"] == 0.0
        assert _attributes["lambdaEOS"] == 0.0
        assert _attributes["piA"] == 0.0
        assert _attributes["piC"] == 0.0
        assert _attributes["piCD"] == 0.0
        assert _attributes["piCF"] == 0.0
        assert _attributes["piCR"] == 0.0
        assert _attributes["piCV"] == 0.0
        assert _attributes["piCYC"] == 0.0
        assert _attributes["piE"] == 0.0
        assert _attributes["piF"] == 0.0
        assert _attributes["piI"] == 0.0
        assert _attributes["piK"] == 0.0
        assert _attributes["piL"] == 0.0
        assert _attributes["piM"] == 0.0
        assert _attributes["piMFG"] == 0.0
        assert _attributes["piN"] == 0.0
        assert _attributes["piNR"] == 0.0
        assert _attributes["piP"] == 0.0
        assert _attributes["piPT"] == 0.0
        assert _attributes["piQ"] == 0.0
        assert _attributes["piR"] == 0.0
        assert _attributes["piS"] == 0.0
        assert _attributes["piT"] == 0.0
        assert _attributes["piTAPS"] == 0.0
        assert _attributes["piU"] == 0.0
        assert _attributes["piV"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["piA"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["piA"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
