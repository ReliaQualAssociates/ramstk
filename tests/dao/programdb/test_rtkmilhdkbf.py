# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkmilhdbkf.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKMilHdbkF module algorithms and models. """

import pytest

from rtk.dao.RTKMilHdbkF import RTKMilHdbkF

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'piP': 0.0,
    'piC': 0.0,
    'piPT': 0.0,
    'piR': 0.0,
    'piA': 0.0,
    'piK': 0.0,
    'lambdaEOS': 0.0,
    'piNR': 0.0,
    'piCF': 0.0,
    'piMFG': 0.0,
    'piM': 0.0,
    'piI': 0.0,
    'lambdaBP': 0.0,
    'piL': 0.0,
    'piCYC': 0.0,
    'piN': 0.0,
    'piF': 0.0,
    'lambdaCYC': 0.0,
    'piCV': 0.0,
    'hardware_id': 1,
    'piE': 0.0,
    'piCR': 0.0,
    'A1': 0.0,
    'piQ': 0.0,
    'A2': 0.0,
    'B1': 0.0,
    'B2': 0.0,
    'lambdaBD': 0.0,
    'piCD': 0.0,
    'C2': 0.0,
    'C1': 0.0,
    'piS': 0.0,
    'piT': 0.0,
    'piU': 0.0,
    'piV': 0.0,
    'piTAPS': 0.0
}


@pytest.mark.integration
def test_rtkmilhdbkf_create(test_dao):
    """ __init__() should create an RTKMilHdbkF model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMilHdbkF).first()

    assert isinstance(DUT, RTKMilHdbkF)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_mil_hdbk_f'
    assert DUT.hardware_id == 1
    assert DUT.A1 == 0.0
    assert DUT.A2 == 0.0
    assert DUT.B1 == 0.0
    assert DUT.B2 == 0.0
    assert DUT.C1 == 0.0
    assert DUT.C2 == 0.0
    assert DUT.lambdaBD == 0.0
    assert DUT.lambdaBP == 0.0
    assert DUT.lambdaCYC == 0.0
    assert DUT.lambdaEOS == 0.0
    assert DUT.piA == 0.0
    assert DUT.piC == 0.0
    assert DUT.piCD == 0.0
    assert DUT.piCF == 0.0
    assert DUT.piCR == 0.0
    assert DUT.piCV == 0.0
    assert DUT.piCYC == 0.0
    assert DUT.piE == 0.0
    assert DUT.piF == 0.0
    assert DUT.piI == 0.0
    assert DUT.piK == 0.0
    assert DUT.piL == 0.0
    assert DUT.piM == 0.0
    assert DUT.piMFG == 0.0
    assert DUT.piN == 0.0
    assert DUT.piNR == 0.0
    assert DUT.piP == 0.0
    assert DUT.piPT == 0.0
    assert DUT.piQ == 0.0
    assert DUT.piR == 0.0
    assert DUT.piS == 0.0
    assert DUT.piT == 0.0
    assert DUT.piTAPS == 0.0
    assert DUT.piU == 0.0
    assert DUT.piV == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMilHdbkF).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMilHdbkF).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKMilHdbkF {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKMilHdbkF).first()

    ATTRIBUTES.pop('B1')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'B1' in attribute "
                    "dictionary passed to RTKMilHdbkF.set_attributes().")

    ATTRIBUTES['B1'] = 0.0
