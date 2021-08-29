# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.site_info.site_info_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKSiteInfoRecord, RAMSTKSiteInfoTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_common_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSiteInfoTable()
    dut.do_connect(mock_common_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_option_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_option_attributes")
    pub.unsubscribe(dut.do_update, "request_update_option")
    pub.unsubscribe(dut.do_get_tree, "request_get_option_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_option_attributes2")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKSiteInfoRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_site_info"
        assert test_recordmodel.site_name == "DEMO SITE"
        assert test_recordmodel.product_key == "DEMO"
        assert test_recordmodel.expire_on == date.today() + timedelta(30)
        assert test_recordmodel.function_enabled == 1
        assert test_recordmodel.requirement_enabled == 1
        assert test_recordmodel.hardware_enabled == 1
        assert test_recordmodel.software_enabled == 0
        assert test_recordmodel.rcm_enabled == 0
        assert test_recordmodel.testing_enabled == 0
        assert test_recordmodel.incident_enabled == 0
        assert test_recordmodel.survival_enabled == 0
        assert test_recordmodel.vandv_enabled == 1
        assert test_recordmodel.hazard_enabled == 1
        assert test_recordmodel.stakeholder_enabled == 1
        assert test_recordmodel.allocation_enabled == 1
        assert test_recordmodel.similar_item_enabled == 1
        assert test_recordmodel.fmea_enabled == 1
        assert test_recordmodel.pof_enabled == 1
        assert test_recordmodel.rbd_enabled == 0
        assert test_recordmodel.fta_enabled == 0

    @pytest.mark.unit
    def test_data_manager_create(self, test_tablemodel):
        """__init__() should return a Options data manager."""
        assert isinstance(test_tablemodel, RAMSTKSiteInfoTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._lst_id_columns == [
            "site_id",
        ]
        assert test_tablemodel._tag == "option"
        assert test_tablemodel._root == 0

        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_option")
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes, "request_get_option_attributes"
        )
        assert pub.isSubscribed(test_tablemodel.do_get_tree, "request_get_option_tree")
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "request_set_option_attributes"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfoRecord instances on success."""
        test_tablemodel.do_select_all({"site_id": 1})

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["option"], RAMSTKSiteInfoRecord
        )
        # There should be a root node with no data package and a node with
        # the one RAMSTKSiteInfoRecord record.
        assert len(test_tablemodel.tree.all_nodes()) == 2

    @pytest.mark.unit
    def test_do_select(self, test_tablemodel):
        """do_select() should return an instance of the RAMSTKSiteInfoRecord on
        success."""
        test_tablemodel.do_select_all({"site_id": 1})

        _options = test_tablemodel.do_select(1)

        assert isinstance(_options, RAMSTKSiteInfoRecord)
        assert _options.site_id == 1
        assert _options.site_name == "DEMO SITE"
        assert _options.product_key == "DEMO"
        assert _options.expire_on == date.today() + timedelta(30)
        assert _options.function_enabled == 1
        assert _options.requirement_enabled == 1
        assert _options.hardware_enabled == 1
        assert _options.software_enabled == 0
        assert _options.rcm_enabled == 0
        assert _options.testing_enabled == 0
        assert _options.incident_enabled == 0
        assert _options.survival_enabled == 0
        assert _options.vandv_enabled == 1
        assert _options.hazard_enabled == 1
        assert _options.stakeholder_enabled == 1
        assert _options.allocation_enabled == 1
        assert _options.similar_item_enabled == 1
        assert _options.fmea_enabled == 1
        assert _options.pof_enabled == 1
        assert _options.rbd_enabled == 0
        assert _options.fta_enabled == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_tablemodel):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        test_tablemodel.do_select_all({"site_id": 1})

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_attributes(self, test_recordmodel):
        """get_attributes() should return a tuple of attribute values."""
        _attributes = test_recordmodel.get_attributes()
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

    @pytest.mark.unit
    def test_set_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should return a zero error code on success."""
        test_attributes.pop("site_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, test_attributes, test_recordmodel):
        """set_attributes() should set an attribute to it's default value when the
        attribute is passed with a None value."""
        test_attributes["fmea_enabled"] = None

        test_attributes.pop("site_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["fmea_enabled"] == 0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, test_attributes, test_recordmodel):
        """set_attributes() should raise an AttributeError when passed an unknown
        attribute."""
        test_attributes.pop("site_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
