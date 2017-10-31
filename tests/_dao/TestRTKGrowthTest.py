#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKGrowthTest.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKGrowthTest module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKGrowthTest import RTKGrowthTest

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKGrowthTest(unittest.TestCase):
    """
    Class for testing the RTKGrowthTest class.
    """

    _attributes = (1, 1, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0, date.today(), date.today(), 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKGrowthTest class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKGrowthTest).first()
        self.DUT.p_growth_rate = self._attributes[6]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkgrowthtest_create(self):
        """
        ($f) DUT should create an RTKGrowthTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKGrowthTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_growth_test')
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.i_mi, 0.0)
        self.assertEqual(self.DUT.i_mf, 0.0)
        self.assertEqual(self.DUT.i_ma, 0.0)
        self.assertEqual(self.DUT.i_num_fails, 0)
        self.assertEqual(self.DUT.p_growth_rate, 0.0)
        self.assertEqual(self.DUT.p_ms, 0.0)
        self.assertEqual(self.DUT.p_fef_avg, 0.0)
        self.assertEqual(self.DUT.p_prob, 0.0)
        self.assertEqual(self.DUT.p_mi, 0.0)
        self.assertEqual(self.DUT.p_mf, 0.0)
        self.assertEqual(self.DUT.p_ma, 0.0)
        self.assertEqual(self.DUT.p_test_time, 0.0)
        self.assertEqual(self.DUT.p_num_fails, 0)
        self.assertEqual(self.DUT.p_start_date, date.today())
        self.assertEqual(self.DUT.p_end_date, date.today())
        self.assertEqual(self.DUT.p_weeks, 0.0)
        self.assertEqual(self.DUT.p_test_units, 0)
        self.assertEqual(self.DUT.p_tpu, 0.0)
        self.assertEqual(self.DUT.p_tpupw, 0.0)
        self.assertEqual(self.DUT.o_growth_rate, 0.0)
        self.assertEqual(self.DUT.o_ms, 0.0)
        self.assertEqual(self.DUT.o_fef_avg, 0.0)
        self.assertEqual(self.DUT.o_mi, 0.0)
        self.assertEqual(self.DUT.o_mf, 0.0)
        self.assertEqual(self.DUT.o_ma, 0.0)
        self.assertEqual(self.DUT.o_test_time, 0.0)
        self.assertEqual(self.DUT.o_num_fails, 0)
        self.assertEqual(self.DUT.o_ttff, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKGrowthTest) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKGrowthTest) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, date.today(), date.today(), 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKGrowthTest {0:d} " \
                               "attributes.".format(self.DUT.phase_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKGrowthTest) set_attributes should return a 10 error code when passed the wrong type
        """
        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, date.today(), date.today(), 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 'None', 0.0, 0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKGrowthTest " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKGrowthTest) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, date.today(), date.today(), 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKGrowthTest.set_attributes().")
