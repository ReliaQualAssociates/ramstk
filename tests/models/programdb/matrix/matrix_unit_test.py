# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.action.matrix_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Matrix algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMatrixRecord
from ramstk.models.dbtables import RAMSTKMatrixTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMatrixModels:
    """Class for unit testing Matrix model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Matrix record model instance."""
        assert isinstance(test_record_model, RAMSTKMatrixRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_matrix"
        assert test_record_model.description == "validation-requirement"
        assert test_record_model.column_id == 6
        assert test_record_model.row_id == 3
        assert test_record_model.correlation == 1

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Matrix table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMatrixTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert isinstance(unit_test_table_model.matrix_df, pd.DataFrame)
        assert unit_test_table_model._db_id_colname == "fld_matrix_id"
        assert unit_test_table_model._db_tablename == "ramstk_matrix"
        assert unit_test_table_model._tag == "matrix"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_matrix_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_matrix_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_matrix"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_matrix"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_matrix_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_matrix"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_matrix"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMatrix(UnitTestSelectMethods):
    """Class for unit testing Matrix table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMatrixRecord
    _tag = "matrix"

    @pytest.mark.unit
    def test_do_build_matrix(self, unit_test_table_model):
        """Should create a pandas DataFrame from a list of column and row headers."""
        _column_lst = ["FUN-0001", "PRF-0002"]
        _row_lst = ["RAA-0001", "RFF-0002", "FTA-0005"]

        unit_test_table_model.do_build_matrix(_column_lst, _row_lst)

        assert isinstance(unit_test_table_model.matrix_df["FUN-0001"], pd.Series)
        assert isinstance(unit_test_table_model.matrix_df["PRF-0002"], pd.Series)
        assert unit_test_table_model.matrix_df["FUN-0001"]["RAA-0001"] == 0
        assert unit_test_table_model.matrix_df["FUN-0001"]["RFF-0002"] == 0
        assert unit_test_table_model.matrix_df["FUN-0001"]["FTA-0005"] == 0
        assert unit_test_table_model.matrix_df["PRF-0002"]["RAA-0001"] == 0
        assert unit_test_table_model.matrix_df["PRF-0002"]["RFF-0002"] == 0
        assert unit_test_table_model.matrix_df["PRF-0002"]["FTA-0005"] == 0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertMatrix(UnitTestInsertMethods):
    """Class for unit testing Matrix table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMatrixRecord
    _tag = "matrix"

    @pytest.mark.skip(reason="Matrices are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Matrices are not hierarchical."""
        pass

    @pytest.mark.unit
    def test_do_insert_column(self, unit_test_table_model):
        """Should add a column to the matrix data frame."""
        _column_lst = ["FUN-0001", "PRF-0002"]
        _row_lst = ["RAA-0001", "RFF-0002", "FTA-0005"]

        unit_test_table_model.do_build_matrix(_column_lst, _row_lst)
        unit_test_table_model.do_insert_column("REL-0003")

        assert isinstance(unit_test_table_model.matrix_df["REL-0003"], pd.Series)
        assert unit_test_table_model.matrix_df["REL-0003"]["RAA-0001"] == 0
        assert unit_test_table_model.matrix_df["REL-0003"]["RFF-0002"] == 0
        assert unit_test_table_model.matrix_df["REL-0003"]["FTA-0005"] == 0

    @pytest.mark.unit
    def test_do_insert_row(self, unit_test_table_model):
        """Should add a row to the matrix data frame."""
        _column_lst = ["FUN-0001", "PRF-0002"]
        _row_lst = ["RAA-0001", "RFF-0002", "FTA-0005"]

        unit_test_table_model.do_build_matrix(_column_lst, _row_lst)
        unit_test_table_model.do_insert_row("RAA-0003")

        assert unit_test_table_model.matrix_df["FUN-0001"]["RAA-0003"] == 0
        assert unit_test_table_model.matrix_df["PRF-0002"]["RAA-0003"] == 0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteMatrix(UnitTestDeleteMethods):
    """Class for unit testing Matrix table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMatrixRecord
    _tag = "matrix"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMatrix(UnitTestGetterSetterMethods):
    """Class for unit testing Matrix table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "matrix_id",
    ]
    _test_attr = "description"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "validation-requirement"
        assert _attributes["correlation"] == 1
