# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.action.action_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKActionRecord
from ramstk.models.dbtables import RAMSTKActionTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateActionModels:
    """Class for unit testing Action model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return an Action record model instance."""
        assert isinstance(test_record_model, RAMSTKActionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_action"
        assert test_record_model.description == "Test FMEA Action #1 for Cause ID #3."
        assert test_record_model.action_category == "Detection"
        assert test_record_model.action_owner == ""
        assert test_record_model.action_due_date == date.today() + timedelta(days=30)
        assert test_record_model.action_status == ""
        assert test_record_model.action_taken == ""
        assert test_record_model.action_approved == 0
        assert test_record_model.action_approve_date == date.today() + timedelta(
            days=30
        )
        assert test_record_model.action_closed == 0
        assert test_record_model.action_close_date == date.today() + timedelta(days=30)

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Should return an Action table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKActionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_action_id"
        assert unit_test_table_model._db_tablename == "ramstk_action"
        assert unit_test_table_model._tag == "action"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_action_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_action_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_action"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_action"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_action_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_action"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_action"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectAction(UnitTestSelectMethods):
    """Class for unit testing Action table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKActionRecord
    _tag = "action"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertAction(UnitTestInsertMethods):
    """Class for unit testing Action table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKActionRecord
    _tag = "action"

    @pytest.mark.skip(reason="Actions are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteAction(UnitTestDeleteMethods):
    """Class for unit testing Action table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKActionRecord
    _tag = "action"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterAction(UnitTestGetterSetterMethods):
    """Class for unit testing Action table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "cause_id",
        "action_id",
    ]
    _test_attr = "action_category"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test FMEA Action #1 for Cause ID #3."
        assert _attributes["action_taken"] == ""
