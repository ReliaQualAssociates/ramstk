#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkfailuredefinition.py is part of The RAMSTK
#       Project
#
# All rights reserved.
""" Test class for testing the RAMSTKFailureDefinition module algorithms and models. """

import pytest

from ramstk.dao.programdb.RAMSTKFailureDefinition import RAMSTKFailureDefinition

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'definition_id': 1,
    'definition': 'Failure Definition'
}


@pytest.mark.integration
def test_ramstkfailuredefinition_create(test_dao):
    """ __init__() should create an RAMSTKFailureDefinition model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureDefinition).first()

    assert isinstance(DUT, RAMSTKFailureDefinition)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_failure_definition'
    assert DUT.revision_id == 1
    assert DUT.definition_id == 1
    assert DUT.definition == 'Failure Definition'


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureDefinition).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureDefinition).first()

    ATTRIBUTES['definition'] = 'Test Failure Definition'

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKFailureDefinition {0:d} "
                    "attributes.".format(DUT.definition_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFailureDefinition).first()

    ATTRIBUTES.pop('definition')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'definition' in attribute "
                    "dictionary passed to "
                    "RAMSTKFailureDefinition.set_attributes().")
