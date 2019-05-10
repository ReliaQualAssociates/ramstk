# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkrequirement.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKRequirement module algorithms and models."""

from datetime import date

import pytest

from ramstk.dao.programdb.RAMSTKRequirement import RAMSTKRequirement

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'owner': '',
    'priority': 0,
    'parent_id': 0,
    'requirement_code': 'REL-0001',
    'q_complete_4': 0,
    'requirement_type': '',
    'q_complete_5': 0,
    'validated_date': date.today(),
    'revision_id': 1,
    'requirement_id': 1,
    'q_consistent_8': 0,
    'q_consistent_7': 0,
    'q_consistent_6': 0,
    'q_consistent_5': 0,
    'q_consistent_4': 0,
    'q_consistent_3': 0,
    'q_consistent_2': 0,
    'q_consistent_1': 0,
    'q_clarity_3': 0,
    'specification': '',
    'q_complete_0': 0,
    'q_complete_1': 0,
    'q_complete_2': 0,
    'q_complete_3': 0,
    'page_number': '',
    'figure_number': '',
    'q_complete_6': 0,
    'q_complete_7': 0,
    'q_complete_8': 0,
    'q_complete_9': 0,
    'q_consistent_0': 0,
    'q_clarity_6': 0,
    'q_clarity_7': 0,
    'q_clarity_4': 0,
    'q_clarity_5': 0,
    'q_clarity_2': 0,
    'description': b'',
    'q_clarity_0': 0,
    'q_clarity_1': 0,
    'q_verifiable_4': 0,
    'derived': 0,
    'q_verifiable_0': 0,
    'q_verifiable_1': 0,
    'q_clarity_8': 0,
    'q_verifiable_3': 0,
    'q_verifiable_2': 0,
    'validated': 0,
    'q_verifiable_5': 0
}


@pytest.mark.integration
def test_ramstkrequirement_create(test_dao):
    """ __init__() should create an RAMSTKRequirement model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKRequirement).first()

    assert isinstance(DUT, RAMSTKRequirement)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_requirement'
    assert DUT.revision_id == 1
    assert DUT.requirement_id == 1
    assert DUT.derived == 0
    assert DUT.description == b''
    assert DUT.figure_number == ''
    assert DUT.owner == ''
    assert DUT.page_number == ''
    assert DUT.parent_id == 0
    assert DUT.priority == 0
    assert DUT.requirement_code == 'REL-0001'
    assert DUT.specification == ''
    assert DUT.requirement_type == ''
    assert DUT.validated == 0
    assert DUT.validated_date == date.today()
    assert DUT.q_clarity_0 == 0
    assert DUT.q_clarity_1 == 0
    assert DUT.q_clarity_2 == 0
    assert DUT.q_clarity_3 == 0
    assert DUT.q_clarity_4 == 0
    assert DUT.q_clarity_5 == 0
    assert DUT.q_clarity_6 == 0
    assert DUT.q_clarity_7 == 0
    assert DUT.q_clarity_8 == 0
    assert DUT.q_complete_0 == 0
    assert DUT.q_complete_1 == 0
    assert DUT.q_complete_2 == 0
    assert DUT.q_complete_3 == 0
    assert DUT.q_complete_4 == 0
    assert DUT.q_complete_5 == 0
    assert DUT.q_complete_6 == 0
    assert DUT.q_complete_7 == 0
    assert DUT.q_complete_8 == 0
    assert DUT.q_complete_9 == 0
    assert DUT.q_consistent_0 == 0
    assert DUT.q_consistent_1 == 0
    assert DUT.q_consistent_2 == 0
    assert DUT.q_consistent_3 == 0
    assert DUT.q_consistent_4 == 0
    assert DUT.q_consistent_5 == 0
    assert DUT.q_consistent_6 == 0
    assert DUT.q_consistent_7 == 0
    assert DUT.q_consistent_8 == 0
    assert DUT.q_verifiable_0 == 0
    assert DUT.q_verifiable_1 == 0
    assert DUT.q_verifiable_2 == 0
    assert DUT.q_verifiable_3 == 0
    assert DUT.q_verifiable_4 == 0
    assert DUT.q_verifiable_5 == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKRequirement).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKRequirement).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKRequirement {0:d} "
                    "attributes.".format(DUT.requirement_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKRequirement).first()

    ATTRIBUTES.pop('q_clarity_1')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'q_clarity_1' in attribute "
                    "dictionary passed to RAMSTKMechanism.set_attributes().")

    ATTRIBUTES['q_clarity_1'] = 0


@pytest.mark.integration
def test_create_code(test_dao):
    """ create_code() should return False on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKRequirement).first()

    assert not DUT.create_code('PERF')
    assert DUT.requirement_code == 'PERF-0001'
