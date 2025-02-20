# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.function.function_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module integrations."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFunctionRecord
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
class TestSelectFunction(SystemTestSelectMethods):
    """Class for testing Function table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKFunctionRecord
    _select_id = 1
    _tag = "function"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertFunction(SystemTestInsertMethods):
    """Class for testing Function table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteFunction(SystemTestDeleteMethods):
    """Class for testing Function table do_delete() method."""

    __test__ = True

    _delete_id = 1
    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateFunction(SystemTestUpdateMethods):
    """Class for testing Function table do_update() and do_update_all() methods."""

    __test__ = True

    _record = RAMSTKFunctionRecord
    _tag = "function"
    _update_bad_value_obj = {1: 2.56}
    _update_field_str = "name"
    _update_id = 2
    _update_value_obj = "Test Function"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterFunction(SystemTestGetterSetterMethods):
    """Class for testing Function table getter and setter methods."""

    __test__ = True

    _package = {"function_code": "-"}
    _record = RAMSTKFunctionRecord
    _tag = "function"
    _test_id = 1
