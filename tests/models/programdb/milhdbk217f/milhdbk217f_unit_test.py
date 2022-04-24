# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.milhdbk217f.milhdbk217f_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing MIL-HDBK-217F module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMilHdbk217FRecord
from ramstk.models.dbtables import RAMSTKMILHDBK217FTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMILHDBK217FModels:
    """Class for unit testing MIL-HDBK-217F model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a MIL-HDBK-217F record model instance."""
        assert isinstance(test_record_model, RAMSTKMilHdbk217FRecord)
        assert test_record_model.__tablename__ == "ramstk_mil_hdbk_f"
        assert test_record_model.hardware_id == 1
        assert test_record_model.A1 == 0.0
        assert test_record_model.A2 == 0.0
        assert test_record_model.B1 == 0.0
        assert test_record_model.B2 == 0.0
        assert test_record_model.C1 == 0.0
        assert test_record_model.C2 == 0.0
        assert test_record_model.lambdaBD == 0.0
        assert test_record_model.lambdaBP == 0.0
        assert test_record_model.lambdaCYC == 0.0
        assert test_record_model.lambdaEOS == 0.0
        assert test_record_model.piA == 0.0
        assert test_record_model.piC == 0.0
        assert test_record_model.piCD == 0.0
        assert test_record_model.piCF == 0.0
        assert test_record_model.piCR == 0.0
        assert test_record_model.piCV == 0.0
        assert test_record_model.piCYC == 0.0
        assert test_record_model.piE == 0.0
        assert test_record_model.piF == 0.0
        assert test_record_model.piI == 0.0
        assert test_record_model.piK == 0.0
        assert test_record_model.piL == 0.0
        assert test_record_model.piM == 0.0
        assert test_record_model.piMFG == 0.0
        assert test_record_model.piN == 0.0
        assert test_record_model.piNR == 0.0
        assert test_record_model.piP == 0.0
        assert test_record_model.piPT == 0.0
        assert test_record_model.piQ == 0.0
        assert test_record_model.piR == 0.0
        assert test_record_model.piS == 0.0
        assert test_record_model.piT == 0.0
        assert test_record_model.piTAPS == 0.0
        assert test_record_model.piU == 0.0
        assert test_record_model.piV == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a MIL-HDBK-217F table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMILHDBK217FTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_mil_hdbk_f"
        assert unit_test_table_model._select_msg == "selected_revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._tag == "milhdbk217f"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKMilHdbk217FRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_milhdbk217f_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_milhdbk217f_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_milhdbk217f"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_milhdbk217f"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_milhdbk217f_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_milhdbk217f"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_milhdbk217f"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_milhdbk217f"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMILHDBK217F(UnitTestSelectMethods):
    """Class for unit testing MIL-HDBK-217F table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMilHdbk217FRecord
    _tag = "milhdbk217f"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertMILHDBK217F(UnitTestInsertMethods):
    """Class for unit testing MIL-HDBK-217F table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMilHdbk217FRecord
    _tag = "milhdbk217f"

    @pytest.mark.skip(reason="MIL-HDBK-217F records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because MIL-HDBK-217F records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteMILHDBK217F(UnitTestDeleteMethods):
    """Class for unit testing MIL-HDBK-217F table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMilHdbk217FRecord
    _tag = "milhdbk217f"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMILHDBK217F(UnitTestGetterSetterMethods):
    """Class for unit testing MIL-HDBK-217F table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]

    _test_attr = "piA"
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
