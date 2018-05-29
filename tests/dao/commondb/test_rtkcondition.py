# * coding: utf8 *
#
#       tests.dao.commondb.test_rtkcondition.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKCondition module algorithms and models."""

import pytest

from rtk.dao.commondb.RTKCondition import RTKCondition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'condition_type': u'operating',
    'condition_id': 1,
    'description': u'Cavitation'
}


@pytest.mark.integration
def test_rtkcondition_create(test_common_dao):
    """ __init__() should create an RTKCondition model. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCondition).first()

    assert isinstance(DUT, RTKCondition)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_condition'
    assert DUT.condition_id == 1
    assert DUT.description == 'Cavitation'
    assert DUT.cond_type == 'operating'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCondition).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCondition).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKCondition {0:d} "
                    "attributes.".format(DUT.condition_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKCondition).first()

    ATTRIBUTES.pop('condition_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'condition_type' in "
                    "attribute dictionary passed to "
                    "RTKCondition.set_attributes().")

    ATTRIBUTES['condition_type'] = u'operating'
