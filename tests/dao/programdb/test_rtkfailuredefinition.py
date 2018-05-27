#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkfailuredefinition.py is part of The RTK
#       Project
#
# All rights reserved.
""" Test class for testing the RTKFailureDefinition module algorithms and models. """

import pytest

from rtk.dao.programdb.RTKFailureDefinition import RTKFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'definition_id': 1,
    'definition': 'Failure Definition'
}


@pytest.mark.integration
def test_rtkfailuredefinition_create(test_dao):
    """ __init__() should create an RTKFailureDefinition model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKFailureDefinition).first()

    assert isinstance(DUT, RTKFailureDefinition)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_failure_definition'
    assert DUT.revision_id == 1
    assert DUT.definition_id == 1
    assert DUT.definition == 'Failure Definition'


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKFailureDefinition).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKFailureDefinition).first()

    ATTRIBUTES['definition'] = 'Test Failure Definition'

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKFailureDefinition {0:d} "
                    "attributes.".format(DUT.definition_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKFailureDefinition).first()

    ATTRIBUTES.pop('definition')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'definition' in attribute "
                    "dictionary passed to "
                    "RTKFailureDefinition.set_attributes().")
