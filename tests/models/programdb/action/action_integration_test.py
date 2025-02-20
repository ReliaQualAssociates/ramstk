# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.action.action_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action integrations."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKActionRecord
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
    SystemTestUpdateMethods,
)


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectAction(SystemTestSelectMethods):
    """Class for testing Action table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKActionRecord
    _select_id = 3
    _tag = "action"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertAction(SystemTestInsertMethods):
    """Class for testing Action table do_insert() method."""

    __test__ = True

    _insert_id = 3
    _record = RAMSTKActionRecord
    _tag = "action"

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteAction(SystemTestDeleteMethods):
    """Class for testing Action table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _next_id = 0
    _record = RAMSTKActionRecord
    _tag = "action"

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateAction(SystemTestUpdateMethods):
    """Class for testing Action table do_update() and do_update_all() methods."""

    __test__ = True

    _record = RAMSTKActionRecord
    _tag = "action"
    _update_bad_value_obj = {1: 2}
    _update_field_str = "description"
    _update_id = 2
    _update_value_obj = "Get a clue"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterAction(SystemTestGetterSetterMethods):
    """Class for testing Action table getter and setter methods."""

    __test__ = True

    _package = {"action_owner": "John Jacob Jingleheimer Schmidt"}
    _record = RAMSTKActionRecord
    _tag = "action"
    _test_id = 1
