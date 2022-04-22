# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.function.function_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFunctionRecord
from ramstk.models.dbtables import RAMSTKFunctionTable

# noinspection PyUnresolvedReferences
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateFunction:
    """Class for unit testing Function model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Function record model instance."""
        assert isinstance(test_record_model, RAMSTKFunctionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_function"
        assert test_record_model.revision_id == 1
        assert test_record_model.availability_logistics == 1.0
        assert test_record_model.availability_mission == 1.0
        assert test_record_model.cost == 0.0
        assert test_record_model.function_code == "PRESS-001"
        assert test_record_model.hazard_rate_logistics == 0.0
        assert test_record_model.hazard_rate_mission == 0.0
        assert test_record_model.level == 0
        assert test_record_model.mmt == 0.0
        assert test_record_model.mcmt == 0.0
        assert test_record_model.mpmt == 0.0
        assert test_record_model.mtbf_logistics == 0.0
        assert test_record_model.mtbf_mission == 0.0
        assert test_record_model.mttr == 0.0
        assert test_record_model.name == "Function Name"
        assert test_record_model.parent_id == 0
        assert test_record_model.remarks == ""
        assert test_record_model.safety_critical == 0
        assert test_record_model.total_mode_count == 0
        assert test_record_model.total_part_count == 0
        assert test_record_model.type_id == 0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Function table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKFunctionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_function_id"
        assert unit_test_table_model._db_tablename == "ramstk_function"
        assert unit_test_table_model._tag == "function"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_function"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_function"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_function_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_function_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_function_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_function"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_function"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectFunction(UnitTestSelectMethods):
    """Class for unit testing Function table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertFunction(UnitTestInsertMethods):
    """Class for unit testing Function table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteFunction(UnitTestDeleteMethods):
    """Class for unit testing Function table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterFunction(UnitTestGetterSetterMethods):
    """Class for unit testing Function table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "function_id",
        "parent_id",
    ]

    _test_attr = "safety_critical"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["availability_logistics"] == 1.0
        assert _attributes["availability_mission"] == 1.0
        assert _attributes["cost"] == 0.0
        assert _attributes["function_code"] == "PRESS-001"
        assert _attributes["hazard_rate_logistics"] == 0.0
        assert _attributes["hazard_rate_mission"] == 0.0
        assert _attributes["level"] == 0
        assert _attributes["mmt"] == 0.0
        assert _attributes["mcmt"] == 0.0
        assert _attributes["mpmt"] == 0.0
        assert _attributes["mtbf_logistics"] == 0.0
        assert _attributes["mtbf_mission"] == 0.0
        assert _attributes["mttr"] == 0.0
        assert _attributes["name"] == "Function Name"
        assert _attributes["parent_id"] == 0
        assert _attributes["remarks"] == ""
        assert _attributes["safety_critical"] == 0
        assert _attributes["total_mode_count"] == 0
        assert _attributes["total_part_count"] == 0
        assert _attributes["type_id"] == 0
