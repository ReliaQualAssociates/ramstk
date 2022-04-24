# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opload.opload_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Load algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpLoadRecord
from ramstk.models.dbtables import RAMSTKOpLoadTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateOpLoadModels:
    """Class for unit testing Operating Load model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return an OpLoad record model instance."""
        assert isinstance(test_record_model, RAMSTKOpLoadRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_op_load"
        assert test_record_model.damage_model == 3
        assert test_record_model.description == "Test Operating Load #1"
        assert test_record_model.priority_id == 0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a OpLoad table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKOpLoadTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_opload_id"
        assert unit_test_table_model._db_tablename == "ramstk_op_load"
        assert unit_test_table_model._tag == "opload"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_opload_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_opload_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_opload"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_opload"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_opload_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_opload"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_opload"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectOpLoad(UnitTestSelectMethods):
    """Class for unit testing OpLoad table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKOpLoadRecord
    _tag = "opload"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertOpLoad(UnitTestInsertMethods):
    """Class for unit testing OpLoad table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKOpLoadRecord
    _tag = "opload"

    @pytest.mark.skip(reason="OpLoad records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because OpLoad records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteOpLoad(UnitTestDeleteMethods):
    """Class for unit testing OpLoad table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKOpLoadRecord
    _tag = "opload"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterOpLoad(UnitTestGetterSetterMethods):
    """Class for unit testing OpLoad table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "opload_id",
    ]

    _test_attr = "priority_id"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test Operating Load #1"
        assert _attributes["damage_model"] == 3
        assert _attributes["priority_id"] == 0
