# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkfailuremode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the RAMSTKFailureMode module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKFailureMode

ATTRIBUTES = {"description": "Parameter Change", "source": "FMD-97", "mode_ratio": 0.2}


@pytest.mark.usefixtures("test_common_dao")
class TestRAMSTKFailureMode:
    """Class for testing the RAMSTKFailureMode model."""

    @pytest.mark.integration
    def test_ramstkfailuremode_create(self, test_common_dao):
        """ __init__() should create an RAMSTKFailureMode model. """
        DUT = test_common_dao.session.query(RAMSTKFailureMode).first()

        assert isinstance(DUT, RAMSTKFailureMode)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == "ramstk_failure_mode"
        assert DUT.category_id == 3
        assert DUT.subcategory_id == 24
        assert DUT.mode_id == 3
        assert DUT.description == "Parameter Change"
        assert DUT.mode_ratio == 0.2
        assert DUT.source == "FMD-97"

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = test_common_dao.session.query(RAMSTKFailureMode).first()

        _attributes = DUT.get_attributes()
        assert _attributes["description"] == "Parameter Change"
        assert _attributes["subcategory_id"] == 24
        assert _attributes["source"] == "FMD-97"
        assert _attributes["category_id"] == 3
        assert _attributes["mode_ratio"] == 0.2

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_common_dao.session.query(RAMSTKFailureMode).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_common_dao.session.query(RAMSTKFailureMode).first()

        ATTRIBUTES["description"] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()["description"] == "Failure Mode Description"

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_common_dao.session.query(RAMSTKFailureMode).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({"shibboly-bibbly-boo": 0.9998})
