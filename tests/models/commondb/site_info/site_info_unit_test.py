# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.site_info.site_info_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Site Information module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSiteInfoRecord
from ramstk.models.dbtables import RAMSTKSiteInfoTable
from tests import MockDAO, UnitTestGetterSetterMethods, UnitTestSelectMethods


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateSiteInfoModels:
    """Class for unit testing Site Information model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Should return a Site Information record model instance."""
        assert isinstance(test_record_model, RAMSTKSiteInfoRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_site_info"
        assert test_record_model.site_name == "DEMO SITE"
        assert test_record_model.product_key == "DEMO"
        assert test_record_model.expire_on == date.today() + timedelta(30)
        assert test_record_model.function_enabled == 1
        assert test_record_model.requirement_enabled == 1
        assert test_record_model.hardware_enabled == 1
        assert test_record_model.software_enabled == 0
        assert test_record_model.rcm_enabled == 0
        assert test_record_model.testing_enabled == 0
        assert test_record_model.incident_enabled == 0
        assert test_record_model.survival_enabled == 0
        assert test_record_model.vandv_enabled == 1
        assert test_record_model.hazard_enabled == 1
        assert test_record_model.stakeholder_enabled == 1
        assert test_record_model.allocation_enabled == 1
        assert test_record_model.similar_item_enabled == 1
        assert test_record_model.fmea_enabled == 1
        assert test_record_model.pof_enabled == 1
        assert test_record_model.rbd_enabled == 0
        assert test_record_model.fta_enabled == 0

    @pytest.mark.unit
    def test_data_manager_create(self, unit_test_table_model):
        """Should return a Site Information table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKSiteInfoTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._lst_id_columns == [
            "site_id",
        ]
        assert unit_test_table_model._tag == "option"
        assert unit_test_table_model._root == 0

        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_option"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes, "request_get_option_attributes"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_option_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "request_set_option_attributes"
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectSiteInfo(UnitTestSelectMethods):
    """Class for unit testing Site Info table do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKSiteInfoRecord
    _tag = "option"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterSiteInfo(UnitTestGetterSetterMethods):
    """Class for unit testing Site Information table methods that get or set."""

    __test__ = True

    _id_columns = [
        "site_id",
    ]

    _test_attr = "fmea_enabled"
    _test_default_value = 0

    @pytest.mark.unit
    def test_get_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()
        assert _attributes["site_id"] == 1
        assert _attributes["site_name"] == "DEMO SITE"
        assert _attributes["product_key"] == "DEMO"
        assert _attributes["expire_on"] == date.today() + timedelta(30)
        assert _attributes["function_enabled"] == 1
        assert _attributes["requirement_enabled"] == 1
        assert _attributes["hardware_enabled"] == 1
        assert _attributes["software_enabled"] == 0
        assert _attributes["rcm_enabled"] == 0
        assert _attributes["testing_enabled"] == 0
        assert _attributes["incident_enabled"] == 0
        assert _attributes["survival_enabled"] == 0
        assert _attributes["vandv_enabled"] == 1
        assert _attributes["hazard_enabled"] == 1
        assert _attributes["stakeholder_enabled"] == 1
        assert _attributes["allocation_enabled"] == 1
        assert _attributes["similar_item_enabled"] == 1
        assert _attributes["fmea_enabled"] == 1
        assert _attributes["pof_enabled"] == 1
        assert _attributes["rbd_enabled"] == 0
        assert _attributes["fta_enabled"] == 0
