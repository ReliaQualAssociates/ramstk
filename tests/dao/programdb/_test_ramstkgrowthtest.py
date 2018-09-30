#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKGrowthTest.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKGrowthTest module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RAMSTKGrowthTest import RAMSTKGrowthTest

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKGrowthTest(unittest.TestCase):
    """
    Class for testing the RAMSTKGrowthTest class.
    """

    _attributes = (1, 1, 0.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, date.today(),
                   date.today(), 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0, 0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKGrowthTest class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKGrowthTest).first()
        self.DUT.p_growth_rate = self._attributes[6]

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstkgrowthtest_create(self):
        """
        ($f) DUT should create an RAMSTKGrowthTest model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKGrowthTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_growth_test')
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
        (TestRAMSTKGrowthTest) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKGrowthTest) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, date.today(),
                       date.today(), 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKGrowthTest {0:d} " \
                               "attributes.".format(self.DUT.phase_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKGrowthTest) set_attributes should return a 10 error code when passed the wrong type
        """
        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, date.today(),
                       date.today(), 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       'None', 0.0, 0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more RAMSTKGrowthTest " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKGrowthTest) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, date.today(),
                       date.today(), 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKGrowthTest.set_attributes().")
