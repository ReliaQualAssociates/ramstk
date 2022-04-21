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
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_recordmodel", "unit_test_table_model")
class UnitTestCreateFunctionModels:
    """Class for unit testing Function model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """Should return a Function record model instance."""
        assert isinstance(test_recordmodel, RAMSTKFunctionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_function"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.availability_logistics == 1.0
        assert test_recordmodel.availability_mission == 1.0
        assert test_recordmodel.cost == 0.0
        assert test_recordmodel.function_code == "PRESS-001"
        assert test_recordmodel.hazard_rate_logistics == 0.0
        assert test_recordmodel.hazard_rate_mission == 0.0
        assert test_recordmodel.level == 0
        assert test_recordmodel.mmt == 0.0
        assert test_recordmodel.mcmt == 0.0
        assert test_recordmodel.mpmt == 0.0
        assert test_recordmodel.mtbf_logistics == 0.0
        assert test_recordmodel.mtbf_mission == 0.0
        assert test_recordmodel.mttr == 0.0
        assert test_recordmodel.name == "Function Name"
        assert test_recordmodel.parent_id == 0
        assert test_recordmodel.remarks == ""
        assert test_recordmodel.safety_critical == 0
        assert test_recordmodel.total_mode_count == 0
        assert test_recordmodel.total_part_count == 0
        assert test_recordmodel.type_id == 0

    @pytest.mark.unit
    def unit_test_table_model_create(self, unit_test_table_model):
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
class UnitTestSelectFunction(UnitTestSelectMethods):
    """Class for unit testing Function table do_select() and do_select_all()."""

    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class UnitTestInsertFunction(UnitTestInsertMethods):
    """Class for unit testing Function table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class UnitTestDeleteFunction(UnitTestDeleteMethods):
    """Class for unit testing Function table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class UnitTestGetterSetterFunction:
    """Class for unit testing Function table methods that get or set.

    Because each table model gets and sets unique attributes, these methods must
    be local to the module being tested.
    """

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """Should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

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

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """Should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self,
        test_attributes,
        test_recordmodel,
    ):
        """Should set an attribute to its default value when passed a None value."""
        test_attributes["safety_critical"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["safety_critical"] == 0

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self,
        test_attributes,
        test_recordmodel,
    ):
        """Should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("parent_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
