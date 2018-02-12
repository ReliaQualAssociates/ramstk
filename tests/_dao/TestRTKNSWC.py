#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKNSWC.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKNSWC module algorithms and models."""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from nose.plugins.attrib import attr

from rtk.dao.RTKNSWC import RTKNSWC

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKNSWC(unittest.TestCase):
    """Class for testing the RTKNSWC class."""

    _attributes = {
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

    def setUp(self):
        """(TestRTKNSWC) Set up the test fixture for the RTKNSWC class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKNSWC).first()
        self.DUT.env_factor = 10

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtknswc_create(self):
        """(TestRTKNSWC)  __init__ should create an RTKNSWC model."""
        self.assertTrue(isinstance(self.DUT, RTKNSWC))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_nswc')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.Cac, 0.0)
        self.assertEqual(self.DUT.Calt, 0.0)
        self.assertEqual(self.DUT.Cb, 0.0)
        self.assertEqual(self.DUT.Cbl, 0.0)
        self.assertEqual(self.DUT.Cbt, 0.0)
        self.assertEqual(self.DUT.Cbv, 0.0)
        self.assertEqual(self.DUT.Cc, 0.0)
        self.assertEqual(self.DUT.Ccf, 0.0)
        self.assertEqual(self.DUT.Ccp, 0.0)
        self.assertEqual(self.DUT.Ccs, 0.0)
        self.assertEqual(self.DUT.Ccv, 0.0)
        self.assertEqual(self.DUT.Ccw, 0.0)
        self.assertEqual(self.DUT.Cd, 0.0)
        self.assertEqual(self.DUT.Cdc, 0.0)
        self.assertEqual(self.DUT.Cdl, 0.0)
        self.assertEqual(self.DUT.Cdp, 0.0)
        self.assertEqual(self.DUT.Cds, 0.0)
        self.assertEqual(self.DUT.Cdt, 0.0)
        self.assertEqual(self.DUT.Cdw, 0.0)
        self.assertEqual(self.DUT.Cdy, 0.0)
        self.assertEqual(self.DUT.Ce, 0.0)
        self.assertEqual(self.DUT.Cf, 0.0)
        self.assertEqual(self.DUT.Cg, 0.0)
        self.assertEqual(self.DUT.Cga, 0.0)
        self.assertEqual(self.DUT.Cgl, 0.0)
        self.assertEqual(self.DUT.Cgp, 0.0)
        self.assertEqual(self.DUT.Cgs, 0.0)
        self.assertEqual(self.DUT.Cgt, 0.0)
        self.assertEqual(self.DUT.Cgv, 0.0)
        self.assertEqual(self.DUT.Ch, 0.0)
        self.assertEqual(self.DUT.Ci, 0.0)
        self.assertEqual(self.DUT.Ck, 0.0)
        self.assertEqual(self.DUT.Cl, 0.0)
        self.assertEqual(self.DUT.Clc, 0.0)
        self.assertEqual(self.DUT.Cm, 0.0)
        self.assertEqual(self.DUT.Cmu, 0.0)
        self.assertEqual(self.DUT.Cn, 0.0)
        self.assertEqual(self.DUT.Cnp, 0.0)
        self.assertEqual(self.DUT.Cnw, 0.0)
        self.assertEqual(self.DUT.Cp, 0.0)
        self.assertEqual(self.DUT.Cpd, 0.0)
        self.assertEqual(self.DUT.Cpf, 0.0)
        self.assertEqual(self.DUT.Cpv, 0.0)
        self.assertEqual(self.DUT.Cq, 0.0)
        self.assertEqual(self.DUT.Cr, 0.0)
        self.assertEqual(self.DUT.Crd, 0.0)
        self.assertEqual(self.DUT.Cs, 0.0)
        self.assertEqual(self.DUT.Csc, 0.0)
        self.assertEqual(self.DUT.Csf, 0.0)
        self.assertEqual(self.DUT.Cst, 0.0)
        self.assertEqual(self.DUT.Csv, 0.0)
        self.assertEqual(self.DUT.Csw, 0.0)
        self.assertEqual(self.DUT.Csz, 0.0)
        self.assertEqual(self.DUT.Ct, 0.0)
        self.assertEqual(self.DUT.Cv, 0.0)
        self.assertEqual(self.DUT.Cw, 0.0)
        self.assertEqual(self.DUT.Cy, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKNSWC) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKNSWC) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKNSWC {0:d} "
                         "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKNSWC) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('Csz')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'Csz' in "
                               "attribute dictionary passed to "
                               "RTKNSWC.set_attributes().")

        self._attributes['Csz'] = 0.0
