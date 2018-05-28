#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKUser.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKUser module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKGroup import RTKGroup

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


ATTRIBUTES = {'group_id': 1, 'description':'Engineering, Design', 'group_type':'workgroup'}


@pytest.mark.integration
def test_rtkworkgroup_create(test_common_dao):
    """ __init__() should create an RTKGroup model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKGroup).first()

    assert isinstance(DUT, RTKGroup)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_group'
    assert DUT.group_id == 1
    assert DUT.description == 'Engineering, Design'
    assert DUT.group_type == 'workgroup'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKGroup).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKGroup).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKGroup {0:d} "
                    "attributes.".format(DUT.group_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKGroup).first()

    ATTRIBUTES.pop('group_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'group_type' in attribute "
                    "dictionary passed to RTKGroup.set_attributes().")

    ATTRIBUTES['group_type'] = 'workgroup'
