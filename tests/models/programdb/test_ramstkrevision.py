# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkrevision.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKRevision module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKRevision

ATTRIBUTES = {
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mmt': 0.0,
    'mcmt': 0.0,
    'mpmt': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mttr': 0.0,
    'name': 'Test Revision',
    'reliability_logistics': 1.0,
    'reliability_mission': 1.0,
    'remarks': b'',
    'total_part_count': 1,
    'revision_code': '',
    'program_time': 0.0,
    'program_time_sd': 0.0,
    'program_cost': 0.0,
    'program_cost_sd': 0.0
}


@pytest.mark.integration
def test_ramstkrevision_create(test_dao):
    """ __init__() should create an RAMSTKRevision model. """
    DUT = test_dao.session.query(RAMSTKRevision).first()

    assert isinstance(DUT, RAMSTKRevision)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_revision'
    assert DUT.revision_id == 1
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.cost == 0.0
    assert DUT.cost_failure == 0.0
    assert DUT.cost_hour == 0.0
    assert DUT.hazard_rate_active == 0.0
    assert DUT.hazard_rate_dormant == 0.0
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.hazard_rate_software == 0.0
    assert DUT.mmt == 0.0
    assert DUT.mcmt == 0.0
    assert DUT.mpmt == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mttr == 0.0
    assert DUT.name == 'Test Revision'
    assert DUT.reliability_logistics == 1.0
    assert DUT.reliability_mission == 1.0
    assert DUT.remarks == b''
    assert DUT.total_part_count == 1
    assert DUT.revision_code == ''
    assert DUT.program_time == 0.0
    assert DUT.program_time_sd == 0.0
    assert DUT.program_cost == 0.0
    assert DUT.program_cost_sd == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of {attr name:attr value} pairs. """
    DUT = test_dao.session.query(RAMSTKRevision).first()

    _attributes = DUT.get_attributes()

    assert _attributes['availability_logistics'] == 1.0
    assert _attributes['availability_mission'] == 1.0
    assert _attributes['cost'] == 0.0
    assert _attributes['cost_failure'] == 0.0
    assert _attributes['cost_hour'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0
    assert _attributes['hazard_rate_dormant'] == 0.0
    assert _attributes['hazard_rate_logistics'] == 0.0
    assert _attributes['hazard_rate_mission'] == 0.0
    assert _attributes['hazard_rate_software'] == 0.0
    assert _attributes['mmt'] == 0.0
    assert _attributes['mcmt'] == 0.0
    assert _attributes['mpmt'] == 0.0
    assert _attributes['mtbf_logistics'] == 0.0
    assert _attributes['mtbf_mission'] == 0.0
    assert _attributes['mttr'] == 0.0
    assert _attributes['name'] == 'Test Revision'
    assert _attributes['reliability_logistics'] == 1.0
    assert _attributes['reliability_mission'] == 1.0
    assert _attributes['remarks'] == b''
    assert _attributes['total_part_count'] == 1
    assert _attributes['revision_code'] == ''
    assert _attributes['program_time'] == 0.0
    assert _attributes['program_time_sd'] == 0.0
    assert _attributes['program_cost'] == 0.0
    assert _attributes['program_cost_sd'] == 0.0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    DUT = test_dao.session.query(RAMSTKRevision).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    DUT = test_dao.session.query(RAMSTKRevision).first()

    ATTRIBUTES['mttr'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['mttr'] == 0.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    DUT = test_dao.session.query(RAMSTKRevision).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
