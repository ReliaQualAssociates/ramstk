# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.hazards.hazards_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazard algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKHazardRecord
from ramstk.models.dbtables import RAMSTKHazardTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)

TEST_PROBS = {
    "A": "Level A - Frequent",
    "B": "Level B - Reasonably Probable",
    "C": "Level C - Occasional",
}


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateHazardModels:
    """Class for unit testing Hazard model __init__() methods.

    Because each table model contains unique attributes, these methods must be local to
    the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Hazard record model instance."""
        assert isinstance(test_record_model, RAMSTKHazardRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_hazard_analysis"
        assert test_record_model.revision_id == 1
        assert test_record_model.assembly_effect == ""
        assert test_record_model.assembly_hri == 20
        assert test_record_model.assembly_hri_f == 4
        assert test_record_model.assembly_mitigation == ""
        assert test_record_model.assembly_probability == TEST_PROBS["A"]
        assert test_record_model.assembly_probability_f == TEST_PROBS["B"]
        assert test_record_model.assembly_severity == "Major"
        assert test_record_model.assembly_severity_f == "Medium"
        assert test_record_model.function_1 == "uf1*uf2"
        assert test_record_model.function_2 == "res1/ui1"
        assert test_record_model.function_3 == ""
        assert test_record_model.function_4 == ""
        assert test_record_model.function_5 == ""
        assert test_record_model.potential_cause == ""
        assert test_record_model.potential_hazard == ""
        assert test_record_model.remarks == ""
        assert test_record_model.result_1 == pytest.approx(0.0)
        assert test_record_model.result_2 == pytest.approx(0.0)
        assert test_record_model.result_3 == pytest.approx(0.0)
        assert test_record_model.result_4 == pytest.approx(0.0)
        assert test_record_model.result_5 == pytest.approx(0.0)
        assert test_record_model.system_effect == ""
        assert test_record_model.system_hri == 20
        assert test_record_model.system_hri_f == 20
        assert test_record_model.system_mitigation == ""
        assert test_record_model.system_probability == TEST_PROBS["A"]
        assert test_record_model.system_probability_f == TEST_PROBS["C"]
        assert test_record_model.system_severity == "Medium"
        assert test_record_model.system_severity_f == "Medium"
        assert test_record_model.user_blob_1 == ""
        assert test_record_model.user_blob_2 == ""
        assert test_record_model.user_blob_3 == ""
        assert test_record_model.user_float_1 == pytest.approx(1.5)
        assert test_record_model.user_float_2 == pytest.approx(0.8)
        assert test_record_model.user_float_3 == pytest.approx(0.0)
        assert test_record_model.user_int_1 == 2
        assert test_record_model.user_int_2 == 0
        assert test_record_model.user_int_3 == 0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return a Hazard table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKHazardTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_hazard_id"
        assert unit_test_table_model._db_tablename == "ramstk_hazard_analysis"
        assert unit_test_table_model._tag == "hazard"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "function_id",
            "hazard_id",
        ]
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKHazardRecord
        assert unit_test_table_model.last_id == 0
        assert unit_test_table_model.pkey == "hazard_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_hazard"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_hazard_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_hazard_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_hazard"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_hazard_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_hazard"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_hazard"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_calculate_fha, "request_calculate_fha"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectHazard(UnitTestSelectMethods):
    """Class for unit testing Hazard table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKHazardRecord
    _tag = "hazard"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertHazard(UnitTestInsertMethods):
    """Class for unit testing Hazard table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKHazardRecord
    _tag = "hazard"

    @pytest.mark.skip(reason="Hazard records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Hazard records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteHazard(UnitTestDeleteMethods):
    """Class for unit testing Hazard table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKHazardRecord
    _tag = "hazard"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterHazard(UnitTestGetterSetterMethods):
    """Class for unit testing Hazard table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "function_id",
        "hazard_id",
    ]

    _test_attr = "system_hri_f"
    _test_default_value = 20

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each database
        record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["potential_hazard"] == ""
        assert _attributes["potential_cause"] == ""
        assert _attributes["assembly_effect"] == ""
        assert _attributes["assembly_severity"] == "Major"
        assert _attributes["assembly_probability"] == TEST_PROBS["A"]
        assert _attributes["assembly_hri"] == 20
        assert _attributes["assembly_mitigation"] == ""
        assert _attributes["assembly_severity_f"] == "Medium"
        assert _attributes["assembly_probability_f"] == TEST_PROBS["B"]
        assert _attributes["assembly_hri_f"] == 4
        assert _attributes["function_1"] == "uf1*uf2"
        assert _attributes["function_2"] == "res1/ui1"
        assert _attributes["function_3"] == ""
        assert _attributes["function_4"] == ""
        assert _attributes["function_5"] == ""
        assert _attributes["remarks"] == ""
        assert _attributes["result_1"] == pytest.approx(0.0)
        assert _attributes["result_2"] == pytest.approx(0.0)
        assert _attributes["result_3"] == pytest.approx(0.0)
        assert _attributes["result_4"] == pytest.approx(0.0)
        assert _attributes["result_5"] == pytest.approx(0.0)
        assert _attributes["system_effect"] == ""
        assert _attributes["system_severity"] == "Medium"
        assert _attributes["system_probability"] == TEST_PROBS["A"]
        assert _attributes["system_hri"] == 20
        assert _attributes["system_mitigation"] == ""
        assert _attributes["system_severity_f"] == "Medium"
        assert _attributes["system_probability_f"] == TEST_PROBS["C"]
        assert _attributes["system_hri_f"] == 20
        assert _attributes["user_blob_1"] == ""
        assert _attributes["user_blob_2"] == ""
        assert _attributes["user_blob_3"] == ""
        assert _attributes["user_float_1"] == pytest.approx(1.5)
        assert _attributes["user_float_2"] == pytest.approx(0.8)
        assert _attributes["user_float_3"] == pytest.approx(0.0)
        assert _attributes["user_int_1"] == 2
        assert _attributes["user_int_2"] == 0
        assert _attributes["user_int_3"] == 0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestHazardAnalysisMethods:
    """Class for testing Hazard analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_hri(self, test_attributes, unit_test_table_model):
        """Should calculate the hazard risk index (HRI) hazard analysis."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model._do_calculate_hri(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["assembly_hri"] == 30
        assert _attributes["system_hri"] == 20
        assert _attributes["assembly_hri_f"] == 16
        assert _attributes["system_hri_f"] == 12

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, test_attributes, unit_test_table_model):
        """Should calculate the user-defined hazard analysis."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model._do_calculate_user_defined(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["result_1"] == pytest.approx(1.2)
        assert _attributes["result_2"] == pytest.approx(0.6)

    @pytest.mark.unit
    def test_do_calculate_fha(self, test_attributes, unit_test_table_model):
        """Should calculate the HRI and user-defined hazard analyses."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model.do_calculate_fha(1)
        _attributes = unit_test_table_model.do_select(1).get_attributes()

        assert _attributes["assembly_hri"] == 30
        assert _attributes["system_hri"] == 20
        assert _attributes["assembly_hri_f"] == 16
        assert _attributes["system_hri_f"] == 12
        assert _attributes["result_1"] == pytest.approx(1.2)
        assert _attributes["result_2"] == pytest.approx(0.6)
