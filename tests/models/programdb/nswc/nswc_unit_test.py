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
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateNSWCModels:
    """Class for unit testing NSWC model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a NSWC record model instance."""
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
    def test_table_model_create(self, unit_test_table_model):
        """Return a NSWC table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKNSWCTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_nswc"
        assert unit_test_table_model._select_msg == "selected_revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._tag == "nswc"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKNSWCRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_nswc_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_nswc_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_nswc"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_nswc"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_nswc_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(unit_test_table_model.do_update, "request_update_nswc")
        assert pub.isSubscribed(unit_test_table_model.do_delete, "request_delete_nswc")
        assert pub.isSubscribed(unit_test_table_model.do_insert, "request_insert_nswc")


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectNSWC(UnitTestSelectMethods):
    """Class for unit testing NSWC table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKNSWCRecord
    _tag = "nswc"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertNSWC(UnitTestInsertMethods):
    """Class for unit testing NSWC table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKNSWCRecord
    _tag = "nswc"

    @pytest.mark.skip(reason="NSWC records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because NSWC records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteNSWC(UnitTestDeleteMethods):
    """Class for unit testing NSWC table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKNSWCRecord
    _tag = "nswc"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterNSWC(UnitTestGetterSetterMethods):
    """Class for unit testing NSWC table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]

    _test_attr = "Cpv"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
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
