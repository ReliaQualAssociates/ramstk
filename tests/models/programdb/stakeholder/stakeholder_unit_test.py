# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.stakeholder.stakeholder_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholderRecord
from ramstk.models.dbtables import RAMSTKStakeholderTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateStakeholderModels:
    """Class for unit testing Stakeholder model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Stakeholder record model instance."""
        assert isinstance(test_record_model, RAMSTKStakeholderRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_stakeholder"
        assert test_record_model.revision_id == 1
        assert test_record_model.customer_rank == 1
        assert test_record_model.description == "Stakeholder Input"
        assert test_record_model.group == ""
        assert test_record_model.improvement == 0.0
        assert test_record_model.overall_weight == 0.0
        assert test_record_model.planned_rank == 1
        assert test_record_model.priority == 1
        assert test_record_model.stakeholder == ""
        assert test_record_model.user_float_1 == 1.0
        assert test_record_model.user_float_2 == 1.0
        assert test_record_model.user_float_3 == 1.0
        assert test_record_model.user_float_4 == 1.0
        assert test_record_model.user_float_5 == 1.0

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Stakeholder table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKStakeholderTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert unit_test_table_model._db_id_colname == "fld_stakeholder_id"
        assert unit_test_table_model._db_tablename == "ramstk_stakeholder"
        assert unit_test_table_model._tag == "stakeholder"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "stakeholder_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKStakeholderRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "stakeholder_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_stakeholder"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_stakeholder"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_stakeholder_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_stakeholder_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_stakeholder_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_stakeholder"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_stakeholder"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_stakeholder,
            "request_calculate_stakeholder",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectStakeholder(UnitTestSelectMethods):
    """Class for unit testing Stakeholder table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKStakeholderRecord
    _tag = "stakeholder"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertStakeholder(UnitTestInsertMethods):
    """Class for unit testing Stakeholder table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKStakeholderRecord
    _tag = "stakeholder"

    @pytest.mark.skip(reason="Stakeholder records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Stakeholder records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteStakeholder(UnitTestDeleteMethods):
    """Class for unit testing Stakeholder table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKStakeholderRecord
    _tag = "stakeholder"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterStakeholder(UnitTestGetterSetterMethods):
    """Class for unit testing Stakeholder table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "requirement_id",
        "stakeholder_id",
    ]

    _test_attr = "overall_weight"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["customer_rank"] == 1
        assert _attributes["description"] == "Stakeholder Input"
        assert _attributes["group"] == ""
        assert _attributes["improvement"] == 0.0
        assert _attributes["overall_weight"] == 0.0
        assert _attributes["planned_rank"] == 1
        assert _attributes["priority"] == 1
        assert _attributes["requirement_id"] == 1
        assert _attributes["stakeholder"] == ""
        assert _attributes["user_float_1"] == 1.0
        assert _attributes["user_float_2"] == 1.0
        assert _attributes["user_float_3"] == 1.0
        assert _attributes["user_float_4"] == 1.0
        assert _attributes["user_float_5"] == 1.0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestStakeholderAnalysisMethods:
    """Class for testing Stakeholder analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_improvement(self, test_attributes, unit_test_table_model):
        """Should calculate the record's improvement factor and overall weight."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _stakeholder = unit_test_table_model.do_select(1)
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        unit_test_table_model.do_update(1)

        unit_test_table_model._do_calculate_improvement(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["improvement"] == 1.2
        assert _attributes["overall_weight"] == 12.48
