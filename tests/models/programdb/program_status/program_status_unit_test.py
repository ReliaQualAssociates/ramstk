# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.program_status.program_status_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramStatusRecord
from ramstk.models.dbtables import RAMSTKProgramStatusTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateProgramStatusModels:
    """Class for unit testing Program Status model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Program Status record model instance."""
        assert isinstance(test_record_model, RAMSTKProgramStatusRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_program_status"
        assert test_record_model.revision_id == 1
        assert test_record_model.cost_remaining == 284.98
        assert test_record_model.date_status == date.today() - timedelta(days=1)
        assert test_record_model.time_remaining == 125.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Program Status table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKProgramStatusTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_status_id"
        assert unit_test_table_model._db_tablename == "ramstk_program_status"
        assert unit_test_table_model._tag == "program_status"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_program_status"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_program_status"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_program_status_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_program_status_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_program_status_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_program_status"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_program_status"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_actual_status, "request_get_actual_status"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectProgramStatus(UnitTestSelectMethods):
    """Class for unit testing Program Status table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertProgramStatus(UnitTestInsertMethods):
    """Class for unit testing Program Status table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"

    @pytest.mark.skip(reason="Program Status records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Program Status records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteProgramStatus(UnitTestDeleteMethods):
    """Class for unit testing Program Status table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKProgramStatusRecord
    _tag = "program_status"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterProgramStatus(UnitTestGetterSetterMethods):
    """Class for unit testing Program Status table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "status_id",
    ]

    _test_attr = "time_remaining"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["cost_remaining"] == 284.98
        assert _attributes["date_status"] == date.today() - timedelta(days=1)
        assert _attributes["time_remaining"] == 125.0
