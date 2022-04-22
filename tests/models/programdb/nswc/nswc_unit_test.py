# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.nswc.nswc_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing NSWC module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKNSWCRecord
from ramstk.models.dbtables import RAMSTKNSWCTable

# noinspection PyUnresolvedReferences
from tests import MockDAO


@pytest.fixture(scope="function")
def test_tablemodel(mock_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKNSWCTable()
    dut.do_connect(mock_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_nswc_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_nswc_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_nswc")
    pub.unsubscribe(dut.do_update, "request_update_nswc")
    pub.unsubscribe(dut.do_get_tree, "request_get_nswc_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_nswc")
    pub.unsubscribe(dut.do_insert, "request_insert_nswc")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_record_model", "test_tablemodel")
class TestCreateModels:
    """Class for testing model initialization."""

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """should return a record model instance."""
        assert isinstance(test_record_model, RAMSTKNSWCRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_nswc"
        assert test_record_model.hardware_id == 1
        assert test_record_model.Cac == 0.0
        assert test_record_model.Calt == 0.0
        assert test_record_model.Cb == 0.0
        assert test_record_model.Cbl == 0.0
        assert test_record_model.Cbt == 0.0
        assert test_record_model.Cbv == 0.0
        assert test_record_model.Cc == 0.0
        assert test_record_model.Ccf == 0.0
        assert test_record_model.Ccp == 0.0
        assert test_record_model.Ccs == 0.0
        assert test_record_model.Ccv == 0.0
        assert test_record_model.Ccw == 0.0
        assert test_record_model.Cd == 0.0
        assert test_record_model.Cdc == 0.0
        assert test_record_model.Cdl == 0.0
        assert test_record_model.Cdp == 0.0
        assert test_record_model.Cds == 0.0
        assert test_record_model.Cdt == 0.0
        assert test_record_model.Cdw == 0.0
        assert test_record_model.Cdy == 0.0
        assert test_record_model.Ce == 0.0
        assert test_record_model.Cf == 0.0
        assert test_record_model.Cg == 0.0
        assert test_record_model.Cga == 0.0
        assert test_record_model.Cgl == 0.0
        assert test_record_model.Cgp == 0.0
        assert test_record_model.Cgs == 0.0
        assert test_record_model.Cgt == 0.0
        assert test_record_model.Cgv == 0.0
        assert test_record_model.Ch == 0.0
        assert test_record_model.Ci == 0.0
        assert test_record_model.Ck == 0.0
        assert test_record_model.Cl == 0.0
        assert test_record_model.Clc == 0.0
        assert test_record_model.Cm == 0.0
        assert test_record_model.Cmu == 0.0
        assert test_record_model.Cn == 0.0
        assert test_record_model.Cnp == 0.0
        assert test_record_model.Cnw == 0.0
        assert test_record_model.Cp == 0.0
        assert test_record_model.Cpd == 0.0
        assert test_record_model.Cpf == 0.0
        assert test_record_model.Cpv == 0.0
        assert test_record_model.Cq == 0.0
        assert test_record_model.Cr == 0.0
        assert test_record_model.Crd == 0.0
        assert test_record_model.Cs == 0.0
        assert test_record_model.Csc == 0.0
        assert test_record_model.Csf == 0.0
        assert test_record_model.Cst == 0.0
        assert test_record_model.Csv == 0.0
        assert test_record_model.Csw == 0.0
        assert test_record_model.Csz == 0.0
        assert test_record_model.Ct == 0.0
        assert test_record_model.Cv == 0.0
        assert test_record_model.Cw == 0.0
        assert test_record_model.Cy == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """should return a table manager instance."""
        assert isinstance(test_tablemodel, RAMSTKNSWCTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_hardware_id"
        assert test_tablemodel._db_tablename == "ramstk_nswc"
        assert test_tablemodel._select_msg == "selected_revision"
        assert test_tablemodel._root == 0
        assert test_tablemodel._tag == "nswc"
        assert test_tablemodel._lst_id_columns == [
            "revision_id",
            "hardware_id",
            "parent_id",
        ]
        assert test_tablemodel._revision_id == 0
        assert test_tablemodel._record == RAMSTKNSWCRecord
        assert test_tablemodel.last_id == 0
        assert test_tablemodel.pkey == "hardware_id"
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_nswc_attributes"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_nswc_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_set_attributes, "wvw_editing_nswc")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_nswc"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_nswc_tree")
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_nswc")
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_nswc")
        assert pub.isSubscribed(test_tablemodel.do_insert, "request_insert_nswc")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """should return a record tree populated with DB records."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(2).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert isinstance(
            test_tablemodel.tree.get_node(3).data["nswc"],
            RAMSTKNSWCRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """should return the record for the passed record ID."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _nswc = test_tablemodel.do_select(1)

        assert isinstance(_nswc, RAMSTKNSWCRecord)
        assert _nswc.revision_id == 1
        assert _nswc.hardware_id == 1
        assert _nswc.Calt == 0.0

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

        assert isinstance(_new_record, RAMSTKNSWCRecord)
        assert _new_record.revision_id == 1
        assert _new_record.hardware_id == 1

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a new record to the records tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_attributes["hardware_id"] = 4
        test_attributes["parent_id"] = 1
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 4
        assert isinstance(
            test_tablemodel.tree.get_node(4).data["nswc"],
            RAMSTKNSWCRecord,
        )
        assert test_tablemodel.tree.get_node(4).data["nswc"].revision_id == 1
        assert test_tablemodel.tree.get_node(4).data["nswc"].hardware_id == 4


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


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["Clc"] == 0.0
        assert _attributes["Crd"] == 0.0
        assert _attributes["Cac"] == 0.0
        assert _attributes["Cmu"] == 0.0
        assert _attributes["Ck"] == 0.0
        assert _attributes["Ci"] == 0.0
        assert _attributes["Ch"] == 0.0
        assert _attributes["Cn"] == 0.0
        assert _attributes["Cm"] == 0.0
        assert _attributes["Cl"] == 0.0
        assert _attributes["Cc"] == 0.0
        assert _attributes["Cb"] == 0.0
        assert _attributes["Cg"] == 0.0
        assert _attributes["Cf"] == 0.0
        assert _attributes["Ce"] == 0.0
        assert _attributes["Cd"] == 0.0
        assert _attributes["Cy"] == 0.0
        assert _attributes["Cbv"] == 0.0
        assert _attributes["Cbt"] == 0.0
        assert _attributes["Cs"] == 0.0
        assert _attributes["Cr"] == 0.0
        assert _attributes["Cq"] == 0.0
        assert _attributes["Cp"] == 0.0
        assert _attributes["Cw"] == 0.0
        assert _attributes["Cv"] == 0.0
        assert _attributes["Ct"] == 0.0
        assert _attributes["Cnw"] == 0.0
        assert _attributes["Cnp"] == 0.0
        assert _attributes["Csf"] == 0.0
        assert _attributes["Calt"] == 0.0
        assert _attributes["Csc"] == 0.0
        assert _attributes["Cbl"] == 0.0
        assert _attributes["Csz"] == 0.0
        assert _attributes["Cst"] == 0.0
        assert _attributes["Csw"] == 0.0
        assert _attributes["Csv"] == 0.0
        assert _attributes["Cgl"] == 0.0
        assert _attributes["Cga"] == 0.0
        assert _attributes["Cgp"] == 0.0
        assert _attributes["Cgs"] == 0.0
        assert _attributes["Cgt"] == 0.0
        assert _attributes["Cgv"] == 0.0
        assert _attributes["Ccw"] == 0.0
        assert _attributes["Ccv"] == 0.0
        assert _attributes["Cpd"] == 0.0
        assert _attributes["Ccp"] == 0.0
        assert _attributes["Cpf"] == 0.0
        assert _attributes["Ccs"] == 0.0
        assert _attributes["Ccf"] == 0.0
        assert _attributes["Cpv"] == 0.0
        assert _attributes["Cdc"] == 0.0
        assert _attributes["Cdl"] == 0.0
        assert _attributes["Cdt"] == 0.0
        assert _attributes["Cdw"] == 0.0
        assert _attributes["Cdp"] == 0.0
        assert _attributes["Cds"] == 0.0
        assert _attributes["Cdy"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_record_model):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_record_model
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["Cpv"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        assert test_record_model.set_attributes(test_attributes) is None
        assert test_record_model.get_attributes()["Cpv"] == 0.0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_record_model
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("hardware_id")
        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})
