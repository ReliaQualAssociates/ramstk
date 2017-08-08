#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKNSWC.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKNSWC module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKNSWC import RTKNSWC

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKNSWC(unittest.TestCase):
    """
    Class for testing the RTKNSWC class.
    """

    _attributes =(1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKNSWC class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKNSWC).first()
        self.DUT.env_factor = 10

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtknswc_create(self):
        """
        ($f) DUT should create an RTKNSWC model.
        """

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
        """
        (TestRTKNSWC) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKNSWC) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKNSWC {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKNSWC) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 'zero.zero', 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKNSWC " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKNSWC) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKNSWC.set_attributes().")
