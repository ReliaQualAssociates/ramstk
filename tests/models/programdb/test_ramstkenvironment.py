# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkenvironment.py is part of The RAMSTK
#       Project
#
# All rights reserved.
""" Test class for testing the RAMSTKEnvironment module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKEnvironment

ATTRIBUTES = {
    'high_dwell_time': 0.0,
    'low_dwell_time': 0.0,
    'maximum': 0.0,
    'mean': 0.0,
    'minimum': 0.0,
    'name': 'Condition Name',
    'ramp_rate': 0.0,
    'units': 'Units',
    'variance': 0.0
}


@pytest.mark.integration
def test_ramstkenvironment_create(test_dao):
    """__init__() should create an RAMSTKEnvironment model."""
    DUT = test_dao.session.query(RAMSTKEnvironment).first()

    assert isinstance(DUT, RAMSTKEnvironment)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_environment'
    assert DUT.phase_id == 1
    assert DUT.environment_id == 1
    assert DUT.name == 'Condition Name'
    assert DUT.units == 'Units'
    assert DUT.minimum == 0.0
    assert DUT.maximum == 0.0
    assert DUT.mean == 0.0
    assert DUT.variance == 0.0
    assert DUT.ramp_rate == 0.0
    assert DUT.low_dwell_time == 0.0
    assert DUT.high_dwell_time == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    DUT = test_dao.session.query(RAMSTKEnvironment).first()

    _attributes = DUT.get_attributes()
    assert _attributes['high_dwell_time'] == 0.0
    assert _attributes['low_dwell_time'] == 0.0
    assert _attributes['maximum'] == 0.0
    assert _attributes['mean'] == 0.0
    assert _attributes['minimum'] == 0.0
    assert _attributes['name'] == 'Condition Name'
    assert _attributes['ramp_rate'] == 0.0
    assert _attributes['units'] == 'Units'
    assert _attributes['variance'] == 0.0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    DUT = test_dao.session.query(RAMSTKEnvironment).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    DUT = test_dao.session.query(RAMSTKEnvironment).first()

    ATTRIBUTES['mean'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['mean'] == 0.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    DUT = test_dao.session.query(RAMSTKEnvironment).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
