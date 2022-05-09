# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.user.user_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing User module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKUserRecord
from ramstk.models.dbtables import RAMSTKUserTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateUserModels:
    """Class for unit testing User model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a User record model instance."""
        assert isinstance(test_record_model, RAMSTKUserRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_user"
        assert test_record_model.user_id == 1
        assert test_record_model.user_lname == "Sweetheart"
        assert test_record_model.user_fname == "Monica"
        assert test_record_model.user_email == "monica.sweetheart@myclub.com"
        assert test_record_model.user_phone == "269-867-5309"
        assert test_record_model.user_group_id == "10"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Should return a User table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKUserTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "user_id",
        ]
        assert unit_test_table_model._tag == "user"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_user_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_user_tree"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectUser(UnitTestSelectMethods):
    """Class for unit testing User table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKUserRecord
    _tag = "user"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterType(UnitTestGetterSetterMethods):
    """Class for unit testing Type table methods that get or set."""

    __test__ = True

    _id_columns = [
        "user_id",
    ]

    _test_attr = "user_phone"
    _test_default_value = "867.5309"

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["user_id"] == 1
        assert _attributes["user_lname"] == "Sweetheart"
        assert _attributes["user_fname"] == "Monica"
        assert _attributes["user_email"] == "monica.sweetheart@myclub.com"
        assert _attributes["user_phone"] == "269-867-5309"
        assert _attributes["user_group_id"] == "10"
