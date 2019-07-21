# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkfunction.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKFunction module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb.RAMSTKFunction import RAMSTKFunction

ATTRIBUTES = {
        'type_id': 0,
        'total_part_count': 0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'hazard_rate_mission': 0.0,
        'mpmt': 0.0,
        'parent_id': 0,
        'mtbf_logistics': 0.0,
        'safety_critical': 0,
        'mmt': 0.0,
        'hazard_rate_logistics': 0.0,
        'remarks': b'',
        'mtbf_mission': 0.0,
        'function_code': 'FUNC-0001',
        'name': 'Function Name',
        'level': 0,
        'mttr': 0.0,
        'mcmt': 0.0,
        'availability_logistics': 1.0,
        'total_mode_count': 0
    }


@pytest.mark.integration
def test_ramstkfunction_create(test_dao):
    """ __init__() should create an RAMSTKFunction model. """
    DUT = test_dao.session.query(RAMSTKFunction).first()

    assert isinstance(DUT, RAMSTKFunction)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_function'
    assert DUT.revision_id == 1
    assert DUT.function_id == 1
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.cost == 0.0
    #assert DUT.function_code == 'FUNC-0001'
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.level == 0
    assert DUT.mmt == 0.0
    assert DUT.mcmt == 0.0
    assert DUT.mpmt == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mttr == 0.0
    #assert DUT.name == 'Function Name'
    assert DUT.parent_id == 0
    assert DUT.remarks == b''
    assert DUT.safety_critical == 0
    assert DUT.total_mode_count == 0
    assert DUT.total_part_count == 0
    assert DUT.type_id == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = test_dao.session.query(RAMSTKFunction).first()

    _attributes = DUT.get_attributes()
    assert _attributes['revision_id'] == 1
    assert _attributes['function_id'] == 1
    assert _attributes['availability_logistics'] == 1.0
    assert _attributes['availability_mission'] == 1.0
    assert _attributes['cost'] == 0.0
    #assert _attributes['function_code'] == 'FUNC-0001'
    assert _attributes['hazard_rate_logistics'] == 0.0
    assert _attributes['hazard_rate_mission'] == 0.0
    assert _attributes['level'] == 0
    assert _attributes['mmt'] == 0.0
    assert _attributes['mcmt'] == 0.0
    assert _attributes['mpmt'] == 0.0
    assert _attributes['mtbf_logistics'] == 0.0
    assert _attributes['mtbf_mission'] == 0.0
    assert _attributes['mttr'] == 0.0
    #assert _attributes['name'] == 'Function Name'
    assert _attributes['parent_id'] == 0
    assert _attributes['remarks'] == b''
    assert _attributes['safety_critical'] == 0
    assert _attributes['total_mode_count'] == 0
    assert _attributes['total_part_count'] == 0
    assert _attributes['type_id'] == 0

@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    DUT = test_dao.session.query(RAMSTKFunction).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    DUT = test_dao.session.query(RAMSTKFunction).first()

    ATTRIBUTES['total_mode_count'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['total_mode_count'] == 0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    DUT = test_dao.session.query(RAMSTKFunction).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
