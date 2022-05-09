# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.control.control_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Control algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKControlRecord
from ramstk.models.dbtables import RAMSTKControlTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateControlModels:
    """Class for unit testing Control model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return a Control record model instance."""
        assert isinstance(test_record_model, RAMSTKControlRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_control"
        assert test_record_model.description == "Test FMEA Control #1 for Cause ID #3."
        assert test_record_model.type_id == "Detection"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Control table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKControlTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_control_id"
        assert unit_test_table_model._db_tablename == "ramstk_control"
        assert unit_test_table_model._tag == "control"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_control_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_control_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_control"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_control"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_control_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_control"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_control"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectControl(UnitTestSelectMethods):
    """Class for unit testing Control table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKControlRecord
    _tag = "control"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertControl(UnitTestInsertMethods):
    """Class for unit testing Control table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKControlRecord
    _tag = "control"

    @pytest.mark.skip(reason="Control records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Controls are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteControl(UnitTestDeleteMethods):
    """Class for unit testing Control table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKControlRecord
    _tag = "control"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterControl(UnitTestGetterSetterMethods):
    """Class for unit testing Control table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "cause_id",
        "control_id",
    ]
    _test_attr = "type_id"
    _test_default_value = ""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test FMEA Control #1 for Cause ID #3."
        assert _attributes["type_id"] == "Detection"
