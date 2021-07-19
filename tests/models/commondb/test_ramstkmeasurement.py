# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.test_ramstkmeasurement.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKMeasurement module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKMeasurement

ATTRIBUTES = {
    "code": "CN",
    "description": "Contamination, Concentration",
    "measurement_type": "damage",
}


@pytest.mark.usefixtures("test_common_dao")
class TestRAMSTKMeasurement:
    """Class for testing the RAMSTKMeasurement model."""

    @pytest.mark.integration
    def test_ramstkmeasurement_create(self, test_common_dao):
        """ __init__() should create an RAMSTKMeasurement model. """
        DUT = (
            test_common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .first()
        )

        assert isinstance(DUT, RAMSTKMeasurement)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == "ramstk_measurement"
        assert DUT.measurement_id == 11
        assert DUT.code == "CN"
        assert DUT.description == "Contamination, Concentration"
        assert DUT.measurement_type == "damage"

    @pytest.mark.integration
    def test_get_attributes(self, test_common_dao):
        """ get_attributes() should return a tuple of attributes values on success. """
        DUT = (
            test_common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .first()
        )

        _attributes = DUT.get_attributes()

        assert _attributes["code"] == "CN"
        assert _attributes["description"] == "Contamination, Concentration"
        assert _attributes["measurement_type"] == "damage"

    @pytest.mark.integration
    def test_set_attributes(self, test_common_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = (
            test_common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .first()
        )

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_common_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = (
            test_common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .first()
        )

        ATTRIBUTES["code"] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()["code"] == "Measurement Code"

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_common_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = (
            test_common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .first()
        )

        with pytest.raises(AttributeError):
            DUT.set_attributes({"shibboly-bibbly-boo": 0.9998})
