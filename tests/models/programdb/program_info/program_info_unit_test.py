# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_info.program_info_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Information module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramInfoRecord
from ramstk.models.dbtables import RAMSTKProgramInfoTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateProgramInfoModels:
    """Class for unit testing Program Information model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Program Information record model instance."""
        assert isinstance(test_record_model, RAMSTKProgramInfoRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_program_info"
        assert test_record_model.revision_id == 1
        assert test_record_model.function_active == 1
        assert test_record_model.requirement_active == 1
        assert test_record_model.hardware_active == 1
        assert test_record_model.software_active == 0
        assert test_record_model.rcm_active == 0
        assert test_record_model.testing_active == 0
        assert test_record_model.incident_active == 0
        assert test_record_model.survival_active == 0
        assert test_record_model.vandv_active == 1
        assert test_record_model.hazard_active == 1
        assert test_record_model.stakeholder_active == 1
        assert test_record_model.allocation_active == 1
        assert test_record_model.similar_item_active == 1
        assert test_record_model.fmea_active == 1
        assert test_record_model.pof_active == 1
        assert test_record_model.rbd_active == 0
        assert test_record_model.fta_active == 0
        assert test_record_model.created_on == date.today()
        assert test_record_model.created_by == ""
        assert test_record_model.last_saved == date.today()
        assert test_record_model.last_saved_by == ""

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Program Information table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKProgramInfoTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._tag == "preference"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "request_program_preferences"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_preference"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_preference_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_preference_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_preference_attributes"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectProgramInfo(UnitTestSelectMethods):
    """Class for unit testing Program Info table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKProgramInfoRecord
    _tag = "preference"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterProgramInfo(UnitTestGetterSetterMethods):
    """Class for unit testing Program Information table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
    ]

    _test_attr = "created_on"
    _test_default_value = date.today()

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["function_active"] == 1
        assert _attributes["requirement_active"] == 1
        assert _attributes["hardware_active"] == 1
        assert _attributes["software_active"] == 0
        assert _attributes["rcm_active"] == 0
        assert _attributes["testing_active"] == 0
        assert _attributes["incident_active"] == 0
        assert _attributes["survival_active"] == 0
        assert _attributes["vandv_active"] == 1
        assert _attributes["hazard_active"] == 1
        assert _attributes["stakeholder_active"] == 1
        assert _attributes["allocation_active"] == 1
        assert _attributes["similar_item_active"] == 1
        assert _attributes["fmea_active"] == 1
        assert _attributes["pof_active"] == 1
        assert _attributes["rbd_active"] == 0
        assert _attributes["fta_active"] == 0
        assert _attributes["created_on"] == date.today()
        assert _attributes["created_by"] == ""
        assert _attributes["last_saved"] == date.today()
        assert _attributes["last_saved_by"] == ""
