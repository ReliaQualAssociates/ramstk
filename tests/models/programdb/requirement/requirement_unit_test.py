# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.requirement.requirement_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRequirementRecord
from ramstk.models.dbtables import RAMSTKRequirementTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateRequirementModels:
    """Class for unit testing Requirement model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Requirement record model instance."""
        assert isinstance(test_record_model, RAMSTKRequirementRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_requirement"
        assert test_record_model.revision_id == 1
        assert test_record_model.derived == 0
        assert test_record_model.description == ""
        assert test_record_model.figure_number == ""
        assert test_record_model.owner == 0
        assert test_record_model.page_number == ""
        assert test_record_model.parent_id == 0
        assert test_record_model.priority == 0
        assert test_record_model.requirement_code == "REL.1"
        assert test_record_model.specification == ""
        assert test_record_model.requirement_type == 0
        assert test_record_model.validated == 0
        assert test_record_model.validated_date == date.today()
        assert test_record_model.q_clarity_0 == 0
        assert test_record_model.q_clarity_1 == 0
        assert test_record_model.q_clarity_2 == 0
        assert test_record_model.q_clarity_3 == 0
        assert test_record_model.q_clarity_4 == 0
        assert test_record_model.q_clarity_5 == 0
        assert test_record_model.q_clarity_6 == 0
        assert test_record_model.q_clarity_7 == 0
        assert test_record_model.q_clarity_8 == 0
        assert test_record_model.q_complete_0 == 0
        assert test_record_model.q_complete_1 == 0
        assert test_record_model.q_complete_2 == 0
        assert test_record_model.q_complete_3 == 0
        assert test_record_model.q_complete_4 == 0
        assert test_record_model.q_complete_5 == 0
        assert test_record_model.q_complete_6 == 0
        assert test_record_model.q_complete_7 == 0
        assert test_record_model.q_complete_8 == 0
        assert test_record_model.q_complete_9 == 0
        assert test_record_model.q_consistent_0 == 0
        assert test_record_model.q_consistent_1 == 0
        assert test_record_model.q_consistent_2 == 0
        assert test_record_model.q_consistent_3 == 0
        assert test_record_model.q_consistent_4 == 0
        assert test_record_model.q_consistent_5 == 0
        assert test_record_model.q_consistent_6 == 0
        assert test_record_model.q_consistent_7 == 0
        assert test_record_model.q_consistent_8 == 0
        assert test_record_model.q_verifiable_0 == 0
        assert test_record_model.q_verifiable_1 == 0
        assert test_record_model.q_verifiable_2 == 0
        assert test_record_model.q_verifiable_3 == 0
        assert test_record_model.q_verifiable_4 == 0
        assert test_record_model.q_verifiable_5 == 0

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Requirement table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKRequirementTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_requirement_id"
        assert unit_test_table_model._db_tablename == "ramstk_requirement"
        assert unit_test_table_model._tag == "requirement"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_requirement"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_requirement"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_requirement_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_requirement_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_requirement_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_requirement"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_create_code, "request_create_requirement_code"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_requirement"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_requirement"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectRequirement(UnitTestSelectMethods):
    """Class for unit testing Requirement table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKRequirementRecord
    _tag = "requirement"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertRequirement(UnitTestInsertMethods):
    """Class for unit testing Requirement table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKRequirementRecord
    _tag = "requirement"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteRequirement(UnitTestDeleteMethods):
    """Class for unit testing Requirement table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKRequirementRecord
    _tag = "requirement"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterRequirement(UnitTestGetterSetterMethods):
    """Class for unit testing Requirement table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "requirement_id",
        "parent_id",
    ]

    _test_attr = "priority"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["derived"] == 0
        assert _attributes["description"] == ""
        assert _attributes["figure_number"] == ""
        assert _attributes["owner"] == 0
        assert _attributes["page_number"] == ""
        assert _attributes["parent_id"] == 0
        assert _attributes["priority"] == 0
        assert _attributes["requirement_code"] == "REL.1"
        assert _attributes["specification"] == ""
        assert _attributes["requirement_type"] == 0
        assert _attributes["validated"] == 0
        assert _attributes["validated_date"] == date.today()
        assert _attributes["q_clarity_0"] == 0
        assert _attributes["q_clarity_1"] == 0
        assert _attributes["q_clarity_2"] == 0
        assert _attributes["q_clarity_3"] == 0
        assert _attributes["q_clarity_4"] == 0
        assert _attributes["q_clarity_5"] == 0
        assert _attributes["q_clarity_6"] == 0
        assert _attributes["q_clarity_7"] == 0
        assert _attributes["q_clarity_8"] == 0
        assert _attributes["q_complete_0"] == 0
        assert _attributes["q_complete_1"] == 0
        assert _attributes["q_complete_2"] == 0
        assert _attributes["q_complete_3"] == 0
        assert _attributes["q_complete_4"] == 0
        assert _attributes["q_complete_5"] == 0
        assert _attributes["q_complete_6"] == 0
        assert _attributes["q_complete_7"] == 0
        assert _attributes["q_complete_8"] == 0
        assert _attributes["q_complete_9"] == 0
        assert _attributes["q_consistent_0"] == 0
        assert _attributes["q_consistent_1"] == 0
        assert _attributes["q_consistent_2"] == 0
        assert _attributes["q_consistent_3"] == 0
        assert _attributes["q_consistent_4"] == 0
        assert _attributes["q_consistent_5"] == 0
        assert _attributes["q_consistent_6"] == 0
        assert _attributes["q_consistent_7"] == 0
        assert _attributes["q_consistent_8"] == 0
        assert _attributes["q_verifiable_0"] == 0
        assert _attributes["q_verifiable_1"] == 0
        assert _attributes["q_verifiable_2"] == 0
        assert _attributes["q_verifiable_3"] == 0
        assert _attributes["q_verifiable_4"] == 0
        assert _attributes["q_verifiable_5"] == 0
