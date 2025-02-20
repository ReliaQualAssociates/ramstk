# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.matrix.matrix_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Matrix integrations."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMatrixRecord
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
class TestSelectMatrix(SystemTestSelectMethods):
    """Class for testing Matrix table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKMatrixRecord
    _select_id = 1
    _tag = "matrix"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertMatrix(SystemTestInsertMethods):
    """Class for testing Matrix table do_insert() method."""

    __test__ = True

    _insert_id = 3
    _record = RAMSTKMatrixRecord
    _tag = "matrix"

    @pytest.mark.skip(reason="Matrix records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Matrixs are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Matrix records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Matrixs are not hierarchical."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteMatrix(SystemTestDeleteMethods):
    """Class for testing Matrix table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _next_id = 0
    _record = RAMSTKMatrixRecord
    _tag = "matrix"

    @pytest.mark.skip(reason="Matrix records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Matrixs are not hierarchical."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateMatrix(SystemTestUpdateMethods):
    """Class for testing Matrix table do_update() and do_update_all() methods."""

    __test__ = True

    _record = RAMSTKMatrixRecord
    _tag = "matrix"
    _update_bad_value_obj = {1: 2}
    _update_field_str = "description"
    _update_id = 2
    _update_value_obj = "Get a clue"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterMatrix(SystemTestGetterSetterMethods):
    """Class for testing Matrix table getter and setter methods."""

    __test__ = True

    _package = {"description": "John Jacob Jingleheimer Schmidt"}
    _record = RAMSTKMatrixRecord
    _tag = "matrix"
    _test_id = 1
