# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission.mission_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMissionRecord
from ramstk.models.dbtables import RAMSTKMissionTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateMissionModels:
    """Class for unit testing Mission model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Mission record model instance."""
        assert isinstance(test_record_model, RAMSTKMissionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_mission"
        assert test_record_model.revision_id == 1
        assert test_record_model.description == "Test mission #1"
        assert test_record_model.mission_time == 100.0
        assert test_record_model.time_units == "hours"

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Mission table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKMissionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_mission_id"
        assert unit_test_table_model._db_tablename == "ramstk_mission"
        assert unit_test_table_model._tag == "mission"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_mission_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_mission_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_mission"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_mission"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_mission"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_mission"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectMission(UnitTestSelectMethods):
    """Class for unit testing Mission table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKMissionRecord
    _tag = "mission"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertMission(UnitTestInsertMethods):
    """Class for unit testing Mission table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMissionRecord
    _tag = "mission"

    @pytest.mark.skip(reason="Mission records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Mission records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteMission(UnitTestDeleteMethods):
    """Class for unit testing Mission table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMissionRecord
    _tag = "mission"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterMission(UnitTestGetterSetterMethods):
    """Class for unit testing Mission table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "mission_id",
    ]

    _test_attr = "mission_time"
    _test_default_value = 0.0

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["description"] == "Test mission #1"
        assert _attributes["mission_time"] == 100.0
        assert _attributes["time_units"] == "hours"
