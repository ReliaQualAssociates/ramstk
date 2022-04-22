# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.stakeholders.stakeholders_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholders module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKStakeholdersRecord
from ramstk.models.dbtables import RAMSTKStakeholdersTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateStakeholdersModels:
    """Class for unit testing Stakeholders model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Stakeholders record model instance."""
        assert isinstance(test_record_model, RAMSTKStakeholdersRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_stakeholders"
        assert test_record_model.stakeholders_id == 1
        assert test_record_model.stakeholder == "Customer"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a Stakeholders table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKStakeholdersTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "stakeholders_id",
        ]
        assert unit_test_table_model._tag == "stakeholders"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_stakeholders_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_stakeholders_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectStakeholders(UnitTestSelectMethods):
    """Class for unit testing Stakeholders table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKStakeholdersRecord
    _tag = "stakeholders"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterStakeholders(UnitTestGetterSetterMethods):
    """Class for unit testing Stakeholders table methods that get or set."""

    __test__ = True

    _id_columns = [
        "stakeholders_id",
    ]

    _test_attr = "stakeholder"
    _test_default_value = "Stakeholder"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["stakeholders_id"] == 1
        assert _attributes["stakeholder"] == "Customer"
