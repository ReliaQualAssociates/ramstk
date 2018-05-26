# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.Test_rtkprograminfo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RTKProgramInfo module algorithms and models."""

from datetime import date

import pytest

from rtk.dao.programdb.RTKProgramInfo import RTKProgramInfo

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'vandv_active': 1,
    'fta_active': 0,
    'revision_active': 1,
    'requirement_active': 1,
    'function_active': 1,
    'software_active': 1,
    'last_saved': date.today(),
    'program_id': 1,
    'method': u'STANDARD',
    'survival_active': 1,
    'created_on': date.today(),
    'fraca_active': 1,
    'last_saved_by': u'',
    'hardware_active': 1,
    'rbd_active': 0,
    'rcm_active': 0,
    'created_by': u'',
    'testing_active': 1
}


@pytest.mark.unit
def test_rtkprograminfo_create(test_dao):
    """ __init__() should create an RTKProgramInfo model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramInfo).first()

    assert isinstance(DUT, RTKProgramInfo)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_program_info'
    assert DUT.program_id == 1
    assert DUT.revision_active == 1
    assert DUT.function_active == 1
    assert DUT.requirement_active == 1
    assert DUT.hardware_active == 1
    assert DUT.software_active == 1
    assert DUT.vandv_active == 1
    assert DUT.testing_active == 1
    assert DUT.fraca_active == 1
    assert DUT.survival_active == 1
    assert DUT.rcm_active == 0
    assert DUT.rbd_active == 0
    assert DUT.fta_active == 0
    assert DUT.created_on == date.today()
    assert DUT.created_by == ''
    assert DUT.last_saved == date.today()
    assert DUT.last_saved_by == ''
    assert DUT.method == 'STANDARD'


@pytest.mark.unit
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramInfo).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.unit
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramInfo).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKProgramInfo {0:d} "
                    "attributes.".format(DUT.program_id))


@pytest.mark.unit
def test_set_attributes_too_few_passed(test_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKProgramInfo).first()

    ATTRIBUTES.pop('vandv_active')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 1
    assert _msg == ("RTK ERROR: Missing attribute 'vandv_active' in attribute "
                    "dictionary passed to RTKProgramInfo.set_attributes().")

    ATTRIBUTES['vandv_active'] = 1
