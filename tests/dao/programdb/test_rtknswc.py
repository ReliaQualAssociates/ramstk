# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtknswc.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKNSWC module algorithms and models. """

import pytest

from rtk.dao.RTKNSWC import RTKNSWC

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'Clc': 0.0,
    'Crd': 0.0,
    'Cac': 0.0,
    'Cmu': 0.0,
    'Ck': 0.0,
    'Ci': 0.0,
    'Ch': 0.0,
    'Cn': 0.0,
    'Cm': 0.0,
    'Cl': 0.0,
    'Cc': 0.0,
    'Cb': 0.0,
    'Cg': 0.0,
    'Cf': 0.0,
    'Ce': 0.0,
    'Cd': 0.0,
    'Cy': 0.0,
    'Cbv': 0.0,
    'Cbt': 0.0,
    'Cs': 0.0,
    'Cr': 0.0,
    'Cq': 0.0,
    'Cp': 0.0,
    'Cw': 0.0,
    'Cv': 0.0,
    'Ct': 0.0,
    'Cnw': 0.0,
    'Cnp': 0.0,
    'Csf': 0.0,
    'Calt': 0.0,
    'Csc': 0.0,
    'Cbl': 0.0,
    'Csz': 0.0,
    'Cst': 0.0,
    'Csw': 0.0,
    'Csv': 0.0,
    'Cgl': 0.0,
    'Cga': 0.0,
    'hardware_id': 1,
    'Cgp': 0.0,
    'Cgs': 0.0,
    'Cgt': 0.0,
    'Cgv': 0.0,
    'Ccw': 0.0,
    'Ccv': 0.0,
    'Cpd': 0.0,
    'Ccp': 0.0,
    'Cpf': 0.0,
    'Ccs': 0.0,
    'Ccf': 0.0,
    'Cpv': 0.0,
    'Cdc': 0.0,
    'Cdl': 0.0,
    'Cdt': 0.0,
    'Cdw': 0.0,
    'Cdp': 0.0,
    'Cds': 0.0,
    'Cdy': 0.0
}


@pytest.mark.integration
def test_rtknswc_create(test_dao):
    """ __init__() should create an RTKNSWC model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKNSWC).first()

    assert isinstance(DUT, RTKNSWC)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_nswc'
    assert DUT.hardware_id == 1
    assert DUT.Cac == 0.0
    assert DUT.Calt == 0.0
    assert DUT.Cb == 0.0
    assert DUT.Cbl == 0.0
    assert DUT.Cbt == 0.0
    assert DUT.Cbv == 0.0
    assert DUT.Cc == 0.0
    assert DUT.Ccf == 0.0
    assert DUT.Ccp == 0.0
    assert DUT.Ccs == 0.0
    assert DUT.Ccv == 0.0
    assert DUT.Ccw == 0.0
    assert DUT.Cd == 0.0
    assert DUT.Cdc == 0.0
    assert DUT.Cdl == 0.0
    assert DUT.Cdp == 0.0
    assert DUT.Cds == 0.0
    assert DUT.Cdt == 0.0
    assert DUT.Cdw == 0.0
    assert DUT.Cdy == 0.0
    assert DUT.Ce == 0.0
    assert DUT.Cf == 0.0
    assert DUT.Cg == 0.0
    assert DUT.Cga == 0.0
    assert DUT.Cgl == 0.0
    assert DUT.Cgp == 0.0
    assert DUT.Cgs == 0.0
    assert DUT.Cgt == 0.0
    assert DUT.Cgv == 0.0
    assert DUT.Ch == 0.0
    assert DUT.Ci == 0.0
    assert DUT.Ck == 0.0
    assert DUT.Cl == 0.0
    assert DUT.Clc == 0.0
    assert DUT.Cm == 0.0
    assert DUT.Cmu == 0.0
    assert DUT.Cn == 0.0
    assert DUT.Cnp == 0.0
    assert DUT.Cnw == 0.0
    assert DUT.Cp == 0.0
    assert DUT.Cpd == 0.0
    assert DUT.Cpf == 0.0
    assert DUT.Cpv == 0.0
    assert DUT.Cq == 0.0
    assert DUT.Cr == 0.0
    assert DUT.Crd == 0.0
    assert DUT.Cs == 0.0
    assert DUT.Csc == 0.0
    assert DUT.Csf == 0.0
    assert DUT.Cst == 0.0
    assert DUT.Csv == 0.0
    assert DUT.Csw == 0.0
    assert DUT.Csz == 0.0
    assert DUT.Ct == 0.0
    assert DUT.Cv == 0.0
    assert DUT.Cw == 0.0
    assert DUT.Cy == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKNSWC).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKNSWC).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKNSWC {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKNSWC).first()

    ATTRIBUTES.pop('Csz')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'Csz' in attribute "
                    "dictionary passed to RTKNSWC.set_attributes().")

    ATTRIBUTES['Csz'] = 0.0
