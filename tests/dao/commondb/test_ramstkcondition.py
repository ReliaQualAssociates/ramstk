# * coding: utf8 *
#
#       tests.dao.commondb.test_ramstkcondition.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKCondition module algorithms and models."""

import pytest

from ramstk.dao.commondb.RAMSTKCondition import RAMSTKCondition

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'condition_type': u'operating',
    'condition_id': 1,
    'description': u'Cavitation'
}


@pytest.mark.integration
def test_ramstkcondition_create(test_common_dao):
    """ __init__() should create an RAMSTKCondition model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKCondition).first()

    assert isinstance(DUT, RAMSTKCondition)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_condition'
    assert DUT.condition_id == 1
    assert DUT.description == 'Cavitation'
    assert DUT.cond_type == 'operating'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKCondition).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKCondition).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKCondition {0:d} "
                    "attributes.".format(DUT.condition_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKCondition).first()

    ATTRIBUTES.pop('condition_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'condition_type' in "
                    "attribute dictionary passed to "
                    "RAMSTKCondition.set_attributes().")

    ATTRIBUTES['condition_type'] = u'operating'
