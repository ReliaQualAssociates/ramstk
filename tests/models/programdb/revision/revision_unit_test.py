# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKRevisionRecord
from ramstk.models.dbtables import RAMSTKRevisionTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateRevisionModels:
    """Class for unit testing Revision model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    __test__ = True

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Revision record model instance."""
        assert isinstance(test_record_model, RAMSTKRevisionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_revision"
        assert test_record_model.revision_id == 1
        assert test_record_model.availability_logistics == 0.9986
        assert test_record_model.availability_mission == 0.99934
        assert test_record_model.cost == 12532.15
        assert test_record_model.cost_failure == 3.52e-05
        assert test_record_model.cost_hour == 1.2532
        assert test_record_model.hazard_rate_active == 0.0
        assert test_record_model.hazard_rate_dormant == 0.0
        assert test_record_model.hazard_rate_logistics == 0.0
        assert test_record_model.hazard_rate_mission == 0.0
        assert test_record_model.hazard_rate_software == 0.0
        assert test_record_model.mmt == 0.0
        assert test_record_model.mcmt == 0.0
        assert test_record_model.mpmt == 0.0
        assert test_record_model.mtbf_logistics == 0.0
        assert test_record_model.mtbf_mission == 0.0
        assert test_record_model.mttr == 0.0
        assert test_record_model.name == "Original Revision"
        assert test_record_model.reliability_logistics == 0.99986
        assert test_record_model.reliability_mission == 0.99992
        assert test_record_model.remarks == "This is the original revision."
        assert test_record_model.revision_code == "Rev. -"
        assert test_record_model.program_time == 2562
        assert test_record_model.program_time_sd == 26.83
        assert test_record_model.program_cost == 26492.83
        assert test_record_model.program_cost_sd == 15.62

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Return a Revision table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKRevisionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_revision_id"
        assert unit_test_table_model._db_tablename == "ramstk_revision"
        assert unit_test_table_model._tag == "revision"
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert unit_test_table_model._record == RAMSTKRevisionRecord
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "request_retrieve_revisions"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_revision_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_revision_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_revision_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert, "request_insert_revision"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectRevision(UnitTestSelectMethods):
    """Class for unit testing Revision table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKRevisionRecord
    _tag = "revision"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertRevision(UnitTestInsertMethods):
    """Class for unit testing Revision table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKRevisionRecord
    _tag = "revision"

    @pytest.mark.skip(reason="Revision records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Revision records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteRevision(UnitTestDeleteMethods):
    """Class for unit testing Revision table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKRevisionRecord
    _tag = "revision"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterRevision(UnitTestGetterSetterMethods):
    """Class for unit testing Revision table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
    ]

    _test_attr = "mtbf_mission"
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
        assert _attributes["availability_logistics"] == 0.9986
        assert _attributes["availability_mission"] == 0.99934
        assert _attributes["cost"] == 12532.15
        assert _attributes["cost_failure"] == 3.52e-05
        assert _attributes["cost_hour"] == 1.2532
        assert _attributes["hazard_rate_active"] == 0.0
        assert _attributes["hazard_rate_dormant"] == 0.0
        assert _attributes["hazard_rate_logistics"] == 0.0
        assert _attributes["hazard_rate_mission"] == 0.0
        assert _attributes["hazard_rate_software"] == 0.0
        assert _attributes["mmt"] == 0.0
        assert _attributes["mcmt"] == 0.0
        assert _attributes["mpmt"] == 0.0
        assert _attributes["mtbf_logistics"] == 0.0
        assert _attributes["mtbf_mission"] == 0.0
        assert _attributes["mttr"] == 0.0
        assert _attributes["name"] == "Original Revision"
        assert _attributes["reliability_logistics"] == 0.99986
        assert _attributes["reliability_mission"] == 0.99992
        assert _attributes["remarks"] == "This is the original revision."
        assert _attributes["revision_code"] == "Rev. -"
        assert _attributes["program_time"] == 2562
        assert _attributes["program_time_sd"] == 26.83
        assert _attributes["program_cost"] == 26492.83
        assert _attributes["program_cost_sd"] == 15.62
