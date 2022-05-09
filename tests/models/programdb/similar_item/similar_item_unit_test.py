# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.similar_item.similar_item_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSimilarItemRecord
from ramstk.models.dbtables import RAMSTKSimilarItemTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)

test_change_description = "Test change description for factor #1."


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateSimilarItemModels:
    """Class for unit testing Similar Item model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Similar Item record model instance."""
        assert isinstance(test_record_model, RAMSTKSimilarItemRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_similar_item"
        assert test_record_model.revision_id == 1
        assert test_record_model.hardware_id == 1
        assert test_record_model.change_description_1 == ""
        assert test_record_model.change_description_2 == ""
        assert test_record_model.change_description_3 == ""
        assert test_record_model.change_description_4 == ""
        assert test_record_model.change_description_5 == ""
        assert test_record_model.change_description_6 == ""
        assert test_record_model.change_description_7 == ""
        assert test_record_model.change_description_8 == ""
        assert test_record_model.change_description_9 == ""
        assert test_record_model.change_description_10 == ""
        assert test_record_model.change_factor_1 == 1.0
        assert test_record_model.change_factor_2 == 1.0
        assert test_record_model.change_factor_3 == 1.0
        assert test_record_model.change_factor_4 == 1.0
        assert test_record_model.change_factor_5 == 1.0
        assert test_record_model.change_factor_6 == 1.0
        assert test_record_model.change_factor_7 == 1.0
        assert test_record_model.change_factor_8 == 1.0
        assert test_record_model.change_factor_9 == 1.0
        assert test_record_model.change_factor_10 == 1.0
        assert test_record_model.environment_from_id == 0
        assert test_record_model.environment_to_id == 0
        assert test_record_model.function_1 == "0"
        assert test_record_model.function_2 == "0"
        assert test_record_model.function_3 == "0"
        assert test_record_model.function_4 == "0"
        assert test_record_model.function_5 == "0"
        assert test_record_model.parent_id == 0
        assert test_record_model.similar_item_method_id == 1
        assert test_record_model.quality_from_id == 0
        assert test_record_model.quality_to_id == 0
        assert test_record_model.result_1 == 0.0
        assert test_record_model.result_2 == 0.0
        assert test_record_model.result_3 == 0.0
        assert test_record_model.result_4 == 0.0
        assert test_record_model.result_5 == 0.0
        assert test_record_model.temperature_from == 30.0
        assert test_record_model.temperature_to == 30.0
        assert test_record_model.user_blob_1 == ""
        assert test_record_model.user_blob_2 == ""
        assert test_record_model.user_blob_3 == ""
        assert test_record_model.user_blob_4 == ""
        assert test_record_model.user_blob_5 == ""
        assert test_record_model.user_float_1 == 0.0
        assert test_record_model.user_float_2 == 0.0
        assert test_record_model.user_float_3 == 0.0
        assert test_record_model.user_float_4 == 0.0
        assert test_record_model.user_float_5 == 0.0
        assert test_record_model.user_int_1 == 0
        assert test_record_model.user_int_2 == 0
        assert test_record_model.user_int_3 == 0
        assert test_record_model.user_int_4 == 0
        assert test_record_model.user_int_5 == 0

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Similar Item table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKSimilarItemTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert unit_test_table_model._db_id_colname == "fld_hardware_id"
        assert unit_test_table_model._db_tablename == "ramstk_similar_item"
        assert unit_test_table_model._tag == "similar_item"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "hardware_id",
        ]
        assert unit_test_table_model._record == RAMSTKSimilarItemRecord
        assert unit_test_table_model.pkey == "hardware_id"
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_similar_item_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_similar_item_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_tree, "succeed_calculate_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_similar_item_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_similar_item"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_roll_up_change_descriptions,
            "request_roll_up_change_descriptions",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectSimilarItem(UnitTestSelectMethods):
    """Class for unit testing Similar Item table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKSimilarItemRecord
    _tag = "similar_item"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertSimilarItem(UnitTestInsertMethods):
    """Class for unit testing Similar Item table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKSimilarItemRecord
    _tag = "similar_item"

    @pytest.mark.skip(reason="Similar Item records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Similar Item records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteSimilarItem(UnitTestDeleteMethods):
    """Class for unit testing Similar Item table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKSimilarItemRecord
    _tag = "similiar_item"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterSimilarItem(UnitTestGetterSetterMethods):
    """Class for unit testing Similar Item table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "hardware_id",
    ]

    _test_attr = "function_1"
    _test_default_value = "0"

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["hardware_id"] == 1
        assert _attributes["change_description_1"] == ""
        assert _attributes["change_description_2"] == ""
        assert _attributes["change_description_3"] == ""
        assert _attributes["change_description_4"] == ""
        assert _attributes["change_description_5"] == ""
        assert _attributes["change_description_6"] == ""
        assert _attributes["change_description_7"] == ""
        assert _attributes["change_description_8"] == ""
        assert _attributes["change_description_9"] == ""
        assert _attributes["change_description_10"] == ""
        assert _attributes["change_factor_1"] == 1.0
        assert _attributes["change_factor_2"] == 1.0
        assert _attributes["change_factor_3"] == 1.0
        assert _attributes["change_factor_4"] == 1.0
        assert _attributes["change_factor_5"] == 1.0
        assert _attributes["change_factor_6"] == 1.0
        assert _attributes["change_factor_7"] == 1.0
        assert _attributes["change_factor_8"] == 1.0
        assert _attributes["change_factor_9"] == 1.0
        assert _attributes["change_factor_10"] == 1.0
        assert _attributes["environment_from_id"] == 0
        assert _attributes["environment_to_id"] == 0
        assert _attributes["function_1"] == "0"
        assert _attributes["function_2"] == "0"
        assert _attributes["function_3"] == "0"
        assert _attributes["function_4"] == "0"
        assert _attributes["function_5"] == "0"
        assert _attributes["parent_id"] == 0
        assert _attributes["similar_item_method_id"] == 1
        assert _attributes["quality_from_id"] == 0
        assert _attributes["quality_to_id"] == 0
        assert _attributes["result_1"] == 0.0
        assert _attributes["result_2"] == 0.0
        assert _attributes["result_3"] == 0.0
        assert _attributes["result_4"] == 0.0
        assert _attributes["result_5"] == 0.0
        assert _attributes["temperature_from"] == 30.0
        assert _attributes["temperature_to"] == 30.0
        assert _attributes["user_blob_1"] == ""
        assert _attributes["user_blob_2"] == ""
        assert _attributes["user_blob_3"] == ""
        assert _attributes["user_blob_4"] == ""
        assert _attributes["user_blob_5"] == ""
        assert _attributes["user_float_1"] == 0.0
        assert _attributes["user_float_2"] == 0.0
        assert _attributes["user_float_3"] == 0.0
        assert _attributes["user_float_4"] == 0.0
        assert _attributes["user_float_5"] == 0.0
        assert _attributes["user_int_1"] == 0
        assert _attributes["user_int_2"] == 0
        assert _attributes["user_int_3"] == 0
        assert _attributes["user_int_4"] == 0
        assert _attributes["user_int_5"] == 0


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSimilarItemAnalysisMethods:
    """Class for similar item methods test suite."""

    @pytest.mark.unit
    def test_do_roll_up_change_descriptions(
        self, test_attributes, unit_test_table_model
    ):
        """Should combine all child change descriptions into one for the parent."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _record = unit_test_table_model.do_select(2)
        _record.change_description_1 = "This is change description 1 for assembly 2."
        _record.change_description_2 = "This is change description 2 for assembly 2."
        _record.change_description_3 = "This is change description 3 for assembly 2."

        _record = unit_test_table_model.do_select(3)
        _record.change_description_1 = "This is change description 1 for assembly 3."
        _record.change_description_2 = "This is change description 2 for assembly 3."
        _record.change_description_3 = "This is change description 3 for assembly 3."

        unit_test_table_model.do_roll_up_change_descriptions(1)

        _record = unit_test_table_model.do_select(1)
        assert _record.change_description_1 == (
            "This is change description 1 for assembly 2.\n\nThis is change "
            "description 1 for assembly 3.\n\n"
        )
        assert _record.change_description_2 == (
            "This is change description 2 for assembly 2.\n\nThis is change "
            "description 2 for assembly 3.\n\n"
        )
        assert _record.change_description_3 == (
            "This is change description 3 for assembly 2.\n\nThis is change "
            "description 3 for assembly 3.\n\n"
        )

    @pytest.mark.unit
    def test_do_calculate_topic_633(self, test_attributes, unit_test_table_model):
        """Should calculate the Topic 6.3.3 similar item."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        unit_test_table_model._node_hazard_rate = 0.000628

        _record = unit_test_table_model.do_select(1)
        _record.similar_item_method_id = 1
        _record.change_description_1 = test_change_description
        _record.environment_from_id = 2
        _record.environment_to_id = 3
        _record.quality_from_id = 1
        _record.quality_to_id = 2
        _record.temperature_from = 55.0
        _record.temperature_to = 65.0

        unit_test_table_model._do_calculate_topic_633(1)

        assert _record.change_factor_1 == 0.8
        assert _record.change_factor_2 == 1.4
        assert _record.change_factor_3 == 1.0
        assert _record.result_1 == pytest.approx(0.0005607143)
        assert _record.change_description_1 == test_change_description

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, test_attributes, unit_test_table_model):
        """Should calculate user-defined similar item."""
        unit_test_table_model.do_select_all(attributes=test_attributes)
        unit_test_table_model._node_hazard_rate = 0.000617

        _record = unit_test_table_model.do_select(1)

        _record.similar_item_method_id = 2
        _record.change_description_1 = test_change_description
        _record.change_factor_1 = 0.85
        _record.change_factor_2 = 1.2
        _record.function_1 = "pi1*pi2*hr"
        _record.function_2 = "0"
        _record.function_3 = "0"
        _record.function_4 = "0"
        _record.function_5 = "0"

        unit_test_table_model._do_calculate_user_defined(1)

        assert _record.change_description_1 == test_change_description
        assert _record.change_factor_1 == 0.85
        assert _record.change_factor_2 == 1.2
        assert _record.result_1 == pytest.approx(0.00062934)
