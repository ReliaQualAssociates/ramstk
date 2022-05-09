# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.mode.mode_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure Mode algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKModeRecord
from ramstk.models.dbtables import RAMSTKModeTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateModeModels:
    """Class for unit testing failure Mode model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a failure Mode record model instance."""
        assert isinstance(test_record_model, RAMSTKModeRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_mode"
        assert test_record_model.effect_local == ""
        assert test_record_model.mission == "Default Mission"
        assert test_record_model.other_indications == ""
        assert test_record_model.mode_criticality == 0.0
        assert test_record_model.single_point == 0
        assert test_record_model.design_provisions == ""
        assert test_record_model.type_id == 0
        assert test_record_model.rpn_severity_new == 1
        assert test_record_model.effect_next == ""
        assert test_record_model.detection_method == ""
        assert test_record_model.operator_actions == ""
        assert test_record_model.critical_item == 0
        assert test_record_model.hazard_rate_source == ""
        assert test_record_model.severity_class == ""
        assert test_record_model.description == "Test Failure Mode #1"
        assert test_record_model.mission_phase == ""
        assert test_record_model.mode_probability == ""
        assert test_record_model.remarks == ""
        assert test_record_model.mode_ratio == 0.0
        assert test_record_model.mode_hazard_rate == 0.0
        assert test_record_model.rpn_severity == 1
        assert test_record_model.isolation_method == ""
        assert test_record_model.effect_end == ""
        assert test_record_model.mode_op_time == 0.0
        assert test_record_model.effect_probability == 0.8

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a failure Mode table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKModeTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_mode_id"
        assert unit_test_table_model._db_tablename == "ramstk_mode"
        assert unit_test_table_model._tag == "mode"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._parent_id == 0
        assert unit_test_table_model.last_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_mode_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_mode_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(unit_test_table_model.do_update, "request_update_mode")
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_mode"
        )
        assert pub.isSubscribed(unit_test_table_model.do_delete, "request_delete_mode")
        assert pub.isSubscribed(unit_test_table_model.do_insert, "request_insert_mode")
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_criticality,
            "request_calculate_criticality",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMode(UnitTestSelectMethods):
    """Class for unit testing failure Mode table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKModeRecord
    _tag = "mode"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertMode(UnitTestInsertMethods):
    """Class for unit testing failure Mode table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKModeRecord
    _tag = "mode"

    @pytest.mark.skip(reason="Mode records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because failure Mode records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteMode(UnitTestDeleteMethods):
    """Class for unit testing failure Mode table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKModeRecord
    _tag = "mode"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMode(UnitTestGetterSetterMethods):
    """Class for unit testing failure Mode table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
        "mode_id",
    ]

    _test_attr = "mode_ratio"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["critical_item"] == 0
        assert _attributes["description"] == "Test Failure Mode #1"
        assert _attributes["design_provisions"] == ""
        assert _attributes["detection_method"] == ""
        assert _attributes["effect_end"] == ""
        assert _attributes["effect_local"] == ""
        assert _attributes["effect_next"] == ""
        assert _attributes["effect_probability"] == 0.8
        assert _attributes["hazard_rate_source"] == ""
        assert _attributes["isolation_method"] == ""
        assert _attributes["mission"] == "Default Mission"
        assert _attributes["mission_phase"] == ""
        assert _attributes["mode_criticality"] == 0.0
        assert _attributes["mode_hazard_rate"] == 0.0
        assert _attributes["mode_op_time"] == 0.0
        assert _attributes["mode_probability"] == ""
        assert _attributes["mode_ratio"] == 0.0
        assert _attributes["operator_actions"] == ""
        assert _attributes["other_indications"] == ""
        assert _attributes["remarks"] == ""
        assert _attributes["rpn_severity"] == 1
        assert _attributes["rpn_severity_new"] == 1
        assert _attributes["severity_class"] == ""
        assert _attributes["single_point"] == 0
        assert _attributes["type_id"] == 0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestModeAnalysisMethods:
    """Class for failure Mode analytical method tests."""

    @pytest.mark.unit
    def test_do_calculate_criticality(self, test_attributes, unit_test_table_model):
        """Should calculate the failure Mode hazard rate and Mode criticality."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model.tree.get_node(1).data["mode"].mode_ratio = 0.428
        unit_test_table_model.tree.get_node(1).data["mode"].mode_op_time = 4.2
        unit_test_table_model.tree.get_node(1).data["mode"].effect_probability = 1.0
        unit_test_table_model.tree.get_node(1).data["mode"].severity_class = "III"

        unit_test_table_model.do_calculate_criticality(0.00000682)

        assert unit_test_table_model.tree.get_node(1).data[
            "mode"
        ].mode_hazard_rate == pytest.approx(2.91896e-06)
        assert unit_test_table_model.tree.get_node(1).data[
            "mode"
        ].mode_criticality == pytest.approx(1.2259632e-05)
