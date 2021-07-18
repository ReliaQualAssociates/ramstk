# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkcategory.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKCategory module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKCategory

ATTRIBUTES = {
    "category_type": "hardware",
    "name": "IC",
    "value": 1,
    "description": "Integrated Circuit",
    "harsh_ir_limit": 0.8,
    "mild_ir_limit": 0.9,
    "harsh_pr_limit": 1.0,
    "mild_pr_limit": 1.0,
    "harsh_vr_limit": 1.0,
    "mild_vr_limit": 1.0,
    "harsh_deltat_limit": 0.0,
    "mild_deltat_limit": 0.0,
    "harsh_maxt_limit": 125.0,
    "mild_maxt_limit": 125.0,
}


@pytest.mark.usefixtures("test_common_dao")
class TestRAMSTKCategory:
    """Class for testing the RAMSTKCategory model."""

    @pytest.mark.integration
    def test_ramstkcategory_create(self, test_common_dao):
        """ __init__() should create an RAMSTKCategory model. """
        DUT = test_common_dao.session.query(RAMSTKCategory).first()

        assert isinstance(DUT, RAMSTKCategory)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == "ramstk_category"
        assert DUT.category_id == 1
        assert DUT.name == "IC"
        assert DUT.description == "Integrated Circuit"
        assert DUT.category_type == "hardware"
        assert DUT.value == 1
        assert DUT.harsh_ir_limit == 0.8
        assert DUT.mild_ir_limit == 0.9
        assert DUT.harsh_pr_limit == 1.0
        assert DUT.mild_pr_limit == 1.0
        assert DUT.harsh_vr_limit == 1.0
        assert DUT.mild_vr_limit == 1.0
        assert DUT.harsh_deltat_limit == 0.0
        assert DUT.mild_deltat_limit == 0.0
        assert DUT.harsh_maxt_limit == 125.0
        assert DUT.mild_maxt_limit == 125.0

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKCategory).first()

        _attributes = DUT.get_attributes()
        assert _attributes["category_type"] == "hardware"
        assert _attributes["name"] == "IC"
        assert _attributes["value"] == 1
        assert _attributes["description"] == "Integrated Circuit"
        assert _attributes["harsh_ir_limit"] == 0.8
        assert _attributes["mild_ir_limit"] == 0.9
        assert _attributes["harsh_pr_limit"] == 1.0
        assert _attributes["mild_pr_limit"] == 1.0
        assert _attributes["harsh_vr_limit"] == 1.0
        assert _attributes["mild_vr_limit"] == 1.0
        assert _attributes["harsh_deltat_limit"] == 0.0
        assert _attributes["mild_deltat_limit"] == 0.0
        assert _attributes["harsh_maxt_limit"] == 125.0
        assert _attributes["mild_maxt_limit"] == 125.0

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKCategory).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKCategory).first()

        ATTRIBUTES["mild_deltat_limit"] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()["mild_deltat_limit"] == 0.0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKCategory).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({"shibboly-bibbly-boo": 0.9998})
