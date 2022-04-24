# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.opstress.opstress_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Stress algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKOpStressRecord
from ramstk.models.dbtables import RAMSTKOpStressTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateOpStressModels:
    """Class for unit testing Operating Stress model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return an OpStress record model instance."""
        assert isinstance(test_record_model, RAMSTKOpStressRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_op_stress"
        assert test_record_model.description == "Test Operating Stress #1"
        assert test_record_model.load_history == 2
        assert test_record_model.measurable_parameter == 0
        assert test_record_model.remarks == ""

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a OpStress table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKOpStressTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_opstress_id"
        assert unit_test_table_model._db_tablename == "ramstk_op_stress"
        assert unit_test_table_model._tag == "opstress"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_opstress_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_opstress_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_opstress"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_opstress"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_opstress_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_opstress"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_opstress"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectOpStress(UnitTestSelectMethods):
    """Class for unit testing OpStress table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKOpStressRecord
    _tag = "opstress"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertOpStress(UnitTestInsertMethods):
    """Class for unit testing OpStress table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKOpStressRecord
    _tag = "opstress"

    @pytest.mark.skip(reason="OpStress records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because OpStress records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteOpStress(UnitTestDeleteMethods):
    """Class for unit testing OpStress table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKOpStressRecord
    _tag = "opstress"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterOpStress(UnitTestGetterSetterMethods):
    """Class for unit testing OpStress table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "opload_id",
        "opstress_id",
    ]

    _test_attr = "measurable_parameter"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test Operating Stress #1"
        assert _attributes["load_history"] == 2
        assert _attributes["measurable_parameter"] == 0
        assert _attributes["remarks"] == ""
