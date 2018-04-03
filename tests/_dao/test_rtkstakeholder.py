#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkstakeholder.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKStakeholder module algorithms and models."""

import pytest

from rtk.dao.RTKStakeholder import RTKStakeholder

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
        'user_float_1': 0.0,
        'priority': 1,
        'group': u'',
        'description': 'Test Stakeholder Input',
        'planned_rank': 1,
        'stakeholder': u'',
        'improvement': 0.0,
        'customer_rank': 1,
        'user_float_5': 0.0,
        'user_float_4': 0.0,
        'user_float_3': 0.0,
        'user_float_2': 0.0,
        'stakeholder_id': 1,
        'overall_weight': 0.0,
        'revision_id': 1,
        'requirement_id': 0
    }


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.requirement
@pytest.mark.stakeholder
def test_rtkstakeholder_create(test_dao):
    """ __init__() should create an RTKStakeholder model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholder).first()

    assert isinstance(DUT, RTKStakeholder)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_stakeholder'
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
    assert DUT.user_float_1 == 0.0
    assert DUT.user_float_2 == 0.0
    assert DUT.user_float_3 == 0.0
    assert DUT.user_float_4 == 0.0
    assert DUT.user_float_5 == 0.0


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.requirement
@pytest.mark.stakeholder
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholder).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.requirement
@pytest.mark.stakeholder
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholder).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKStakeholder {0:d} "
                    "attributes.".format(DUT.stakeholder_id))


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.requirement
@pytest.mark.stakeholder
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKStakeholder).first()

    ATTRIBUTES.pop('user_float_1')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'user_float_1' in attribute "
                    "dictionary passed to RTKStakeholder.set_attributes().")

    ATTRIBUTES['user_float_1'] = 0.0
