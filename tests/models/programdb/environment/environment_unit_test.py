# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.environment.environment_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKEnvironmentRecord
from ramstk.models.dbtables import RAMSTKEnvironmentTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateEnvironmentModels:
    """Class for unit testing Environment model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return an Environment record model instance."""
        assert isinstance(test_record_model, RAMSTKEnvironmentRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_environment"
        assert test_record_model.revision_id == 1
        assert test_record_model.name == "Condition Name"
        assert test_record_model.units == "Units"
        assert test_record_model.minimum == 0.0
        assert test_record_model.maximum == 0.0
        assert test_record_model.mean == 0.0
        assert test_record_model.variance == 0.0
        assert test_record_model.ramp_rate == 0.0
        assert test_record_model.low_dwell_time == 0.0
        assert test_record_model.high_dwell_time == 0.0

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return an Environment table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKEnvironmentTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert unit_test_table_model._db_id_colname == "fld_environment_id"
        assert unit_test_table_model._db_tablename == "ramstk_environment"
        assert unit_test_table_model._tag == "environment"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "mission_id",
            "mission_phase_id",
            "environment_id",
        ]
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_environment_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_environment_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_environment"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_environment"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_environment"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_environment"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectEnvironment(UnitTestSelectMethods):
    """Class for unit testing Environment table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKEnvironmentRecord
    _tag = "environment"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertEnvironment(UnitTestInsertMethods):
    """Class for unit testing Environment table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKEnvironmentRecord
    _tag = "environment"

    @pytest.mark.skip(reason="Environment records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Environment records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteEnvironment(UnitTestDeleteMethods):
    """Class for unit testing Environment table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKEnvironmentRecord
    _tag = "environment"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterEnvironment(UnitTestGetterSetterMethods):
    """Class for unit testing Environment table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "mission_id",
        "mission_phase_id",
        "environment_id",
    ]
    _test_attr = "minimum"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["name"] == "Condition Name"
        assert _attributes["units"] == "Units"
        assert _attributes["minimum"] == 0.0
        assert _attributes["maximum"] == 0.0
        assert _attributes["mean"] == 0.0
        assert _attributes["variance"] == 0.0
        assert _attributes["ramp_rate"] == 0.0
        assert _attributes["low_dwell_time"] == 0.0
        assert _attributes["high_dwell_time"] == 0.0
