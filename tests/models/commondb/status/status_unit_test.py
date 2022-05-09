# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.status.status_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStatusRecord
from ramstk.models.dbtables import RAMSTKStatusTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateStatusModels:
    """Class for unit testing Status model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Status record model instance."""
        assert isinstance(test_record_model, RAMSTKStatusRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_status"
        assert test_record_model.status_id == 1
        assert test_record_model.status_type == "action"
        assert test_record_model.name == "Initiated"
        assert test_record_model.description == "Action has been initiated."

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Status table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKStatusTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "status_id",
        ]
        assert unit_test_table_model._tag == "status"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_status_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_status_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectStatus(UnitTestSelectMethods):
    """Class for unit testing Status table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKStatusRecord
    _tag = "status"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterStatus(UnitTestGetterSetterMethods):
    """Class for unit testing Status table methods that get or set."""

    __test__ = True

    _id_columns = [
        "status_id",
    ]

    _test_attr = "name"
    _test_default_value = "Status Name"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["status_id"] == 1
        assert _attributes["status_type"] == "action"
        assert _attributes["name"] == "Initiated"
        assert _attributes["description"] == "Action has been initiated."
