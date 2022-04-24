# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.cause.cause_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord
from ramstk.models.dbtables import RAMSTKCauseTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateCauseModels:
    """Class for unit testing Cause model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return a Cause record model instance."""
        assert isinstance(test_record_model, RAMSTKCauseRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_cause"
        assert (
            test_record_model.description == "Test Failure Cause #1 for Mechanism ID 3"
        )
        assert test_record_model.rpn == 0
        assert test_record_model.rpn_new == 0
        assert test_record_model.rpn_detection == 3
        assert test_record_model.rpn_detection_new == 3
        assert test_record_model.rpn_occurrence_new == 6
        assert test_record_model.rpn_occurrence == 4

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Cause table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKCauseTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_cause_id"
        assert unit_test_table_model._db_tablename == "ramstk_cause"
        assert unit_test_table_model._tag == "cause"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_cause_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_cause_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_cause"
        )
        assert pub.isSubscribed(unit_test_table_model.do_update, "request_update_cause")
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_cause_tree"
        )
        assert pub.isSubscribed(unit_test_table_model.do_delete, "request_delete_cause")
        assert pub.isSubscribed(unit_test_table_model.do_insert, "request_insert_cause")
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_rpn, "request_calculate_cause_rpn"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectCause(UnitTestSelectMethods):
    """Class for unit testing Cause table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKCauseRecord
    _tag = "cause"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertCause(UnitTestInsertMethods):
    """Class for unit testing Cause table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKCauseRecord
    _tag = "cause"

    @pytest.mark.skip(reason="Causes are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Causes are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteCause(UnitTestDeleteMethods):
    """Class for unit testing Cause table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKCauseRecord
    _tag = "cause"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterCause(UnitTestGetterSetterMethods):
    """Class for unit testing Cause table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
        "cause_id",
    ]
    _test_attr = "rpn_detection_new"
    _test_default_value = 10

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["description"] == "Test Failure Cause #1 for Mechanism ID 3"
        assert _attributes["rpn"] == 0
        assert _attributes["rpn_detection"] == 3
        assert _attributes["rpn_detection_new"] == 3
        assert _attributes["rpn_new"] == 0
        assert _attributes["rpn_occurrence"] == 4
        assert _attributes["rpn_occurrence_new"] == 6


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestCauseAnalysisMethods:
    """Class for testing Cause analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, unit_test_table_model):
        """Should calculate the cause RPN."""
        unit_test_table_model.do_select_all(test_attributes)

        unit_test_table_model.tree.get_node(1).data["cause"].rpn_occurrence = 8
        unit_test_table_model.tree.get_node(1).data["cause"].rpn_detection = 3
        unit_test_table_model.tree.get_node(2).data["cause"].rpn_occurrence = 4
        unit_test_table_model.tree.get_node(2).data["cause"].rpn_detection = 5

        unit_test_table_model.do_calculate_rpn(8)

        assert unit_test_table_model.tree.get_node(1).data["cause"].rpn == 192
        assert unit_test_table_model.tree.get_node(2).data["cause"].rpn == 160
