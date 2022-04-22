# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.load_history.load_history_unit_test.py is part of The
#       RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Load History module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKLoadHistoryRecord
from ramstk.models.dbtables import RAMSTKLoadHistoryTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateLoadHistoryModels:
    """Class for unit testing Load History model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Load History record model instance."""
        assert isinstance(test_record_model, RAMSTKLoadHistoryRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_load_history"
        assert test_record_model.history_id == 1
        assert test_record_model.description == "Histogram"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Load History table model."""
        assert isinstance(unit_test_table_model, RAMSTKLoadHistoryTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "history_id",
        ]
        assert unit_test_table_model._tag == "load_history"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_load_history_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_load_history_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectLoadHistory(UnitTestSelectMethods):
    """Class for unit testing Load History table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKLoadHistoryRecord
    _tag = "load_history"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterLoadHistory(UnitTestGetterSetterMethods):
    """Class for unit testing Load History table methods that get or set."""

    __test__ = True

    _id_columns = [
        "history_id",
    ]

    _test_attr = "description"
    _test_default_value = "Load History Description"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["history_id"] == 1
        assert _attributes["description"] == "Histogram"
