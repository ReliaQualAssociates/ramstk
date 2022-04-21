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
import treelib
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFunctionRecord
from ramstk.models.dbtables import RAMSTKFunctionTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
    SystemTestUpdateMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class SystemTestSelectFunction(SystemTestSelectMethods):
    """Class for testing Function table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _tag = "function"
    _record = RAMSTKFunctionRecord


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertFunction(SystemTestInsertMethods):
    """Class for testing Function table do_insert() method."""

    __test__ = True

    _tag = "function"
    _record = RAMSTKFunctionRecord


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteMethods(SystemTestDeleteMethods):
    """Class for testing Function table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateMethods(SystemTestUpdateMethods):
    """Class for testing Function table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFunctionRecord
    _tag = "function"


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetter(SystemTestGetterSetterMethods):
    """Class for testing Function table getter and setter methods."""

    __test__ = True

    _package = {"function_code": "-"}
    _record = RAMSTKFunctionRecord
    _tag = "function"
    _test_id = 1
