# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMechanismRecord
from ramstk.models.dbtables import RAMSTKMechanismTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMechanismModels:
    """Class for unit testing failure Mechanism model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Mechanism record model instance."""
        assert isinstance(test_record_model, RAMSTKMechanismRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_mechanism"
        assert test_record_model.description == "Test Failure Mechanism #1"
        assert test_record_model.rpn == 100
        assert test_record_model.rpn_new == 100
        assert test_record_model.rpn_detection == 10
        assert test_record_model.rpn_detection_new == 10
        assert test_record_model.rpn_occurrence_new == 10
        assert test_record_model.rpn_occurrence == 10
        assert test_record_model.pof_include == 1

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a failure Mechanism table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMechanismTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_mechanism_id"
        assert unit_test_table_model._db_tablename == "ramstk_mechanism"
        assert unit_test_table_model._tag == "mechanism"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_mechanism_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_mechanism_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_mechanism"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_mechanism"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_mechanism_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_mechanism"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_mechanism"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_rpn, "request_calculate_mechanism_rpn"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMechanism(UnitTestSelectMethods):
    """Class for unit testing Mechanism table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMechanismRecord
    _tag = "mechanism"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertMechanism(UnitTestInsertMethods):
    """Class for unit testing Mechanism table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"

    @pytest.mark.skip(reason="Mechanism records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Mechanism records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteMechanism(UnitTestDeleteMethods):
    """Class for unit testing Mechanism table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMechanism(UnitTestGetterSetterMethods):
    """Class for unit testing Mechanism table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
        "mechanism_id",
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
        assert _attributes["description"] == "Test Failure Mechanism #1"
        assert _attributes["pof_include"] == 1
        assert _attributes["rpn"] == 100
        assert _attributes["rpn_detection"] == 10
        assert _attributes["rpn_detection_new"] == 10
        assert _attributes["rpn_new"] == 100
        assert _attributes["rpn_occurrence"] == 10
        assert _attributes["rpn_occurrence_new"] == 10


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestMechanismAnalysisMethods:
    """Class for testing failure Mechanism analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, unit_test_table_model):
        """Should calculate the mechanism RPN."""
        unit_test_table_model.do_select_all(test_attributes)

        unit_test_table_model.tree.get_node(1).data["mechanism"].rpn_occurrence = 8
        unit_test_table_model.tree.get_node(1).data["mechanism"].rpn_detection = 3
        unit_test_table_model.tree.get_node(2).data["mechanism"].rpn_occurrence = 4
        unit_test_table_model.tree.get_node(2).data["mechanism"].rpn_detection = 5

        unit_test_table_model.do_calculate_rpn(8)

        assert unit_test_table_model.tree.get_node(1).data["mechanism"].rpn == 192
        assert unit_test_table_model.tree.get_node(2).data["mechanism"].rpn == 160
