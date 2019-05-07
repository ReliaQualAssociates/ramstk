#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkstakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKStakeholder module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKStakeholder import RAMSTKStakeholder

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'user_float_1': 1.0,
    'priority': 1,
    'group': '',
    'description': 'Test Stakeholder Input',
    'planned_rank': 1,
    'stakeholder': '',
    'improvement': 0.0,
    'customer_rank': 1,
    'user_float_5': 1.0,
    'user_float_4': 1.0,
    'user_float_3': 1.0,
    'user_float_2': 1.0,
    'stakeholder_id': 1,
    'overall_weight': 0.0,
    'revision_id': 1,
    'requirement_id': 0
}


@pytest.mark.integration
def test_ramstkstakeholder_create(test_dao):
    """ __init__() should create an RAMSTKStakeholder model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKStakeholder).first()

    assert isinstance(DUT, RAMSTKStakeholder)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_stakeholder'
    assert DUT.revision_id == 1
    assert DUT.stakeholder_id == 1
    assert DUT.customer_rank == 1
    assert DUT.description == 'Test Stakeholder Input'
    assert DUT.group == ''
    assert DUT.improvement == 0.0
    assert DUT.overall_weight == 0.0
    assert DUT.planned_rank == 1
    assert DUT.priority == 1
    assert DUT.requirement_id == 0
    assert DUT.stakeholder == ''
    assert DUT.user_float_1 == 1.0
    assert DUT.user_float_2 == 1.0
    assert DUT.user_float_3 == 1.0
    assert DUT.user_float_4 == 1.0
    assert DUT.user_float_5 == 1.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKStakeholder).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKStakeholder).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKStakeholder {0:d} "
                    "attributes.".format(DUT.stakeholder_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKStakeholder).first()

    ATTRIBUTES.pop('user_float_1')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'user_float_1' in attribute "
                    "dictionary passed to RAMSTKStakeholder.set_attributes().")

    ATTRIBUTES['user_float_1'] = 0.0
