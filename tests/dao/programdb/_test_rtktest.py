#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKTest.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKTest module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKTest import RTKTest

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKTest(unittest.TestCase):
    """
    Class for testing the RTKTest class.
    """

    _attributes = (1, 1, 0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKTest class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKTest).first()
        self.DUT.description = self._attributes[17]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtktest_create(self):
        """
        (TestRTKTest) __init__ should create an RTKTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_test')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.assess_model_id, 0)
        self.assertEqual(self.DUT.attachment, '')
        self.assertEqual(self.DUT.avg_fef, 0.0)
        self.assertEqual(self.DUT.avg_growth, 0.0)
        self.assertEqual(self.DUT.avg_ms, 0.0)
        self.assertEqual(self.DUT.chi_square, 0.0)
        self.assertEqual(self.DUT.confidence, 0.0)
        self.assertEqual(self.DUT.consumer_risk, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.cum_failures, 0)
        self.assertEqual(self.DUT.cum_mean, 0.0)
        self.assertEqual(self.DUT.cum_mean_ll, 0.0)
        self.assertEqual(self.DUT.cum_mean_se, 0.0)
        self.assertEqual(self.DUT.cum_mean_ul, 0.0)
        self.assertEqual(self.DUT.cum_time, 0.0)
        self.assertEqual(self.DUT.description, 'Test Test Description')
        self.assertEqual(self.DUT.grouped, 0)
        self.assertEqual(self.DUT.group_interval, 0.0)
        self.assertEqual(self.DUT.inst_mean, 0.0)
        self.assertEqual(self.DUT.inst_mean_ll, 0.0)
        self.assertEqual(self.DUT.inst_mean_se, 0.0)
        self.assertEqual(self.DUT.inst_mean_ul, 0.0)
        self.assertEqual(self.DUT.mg, 0.0)
        self.assertEqual(self.DUT.mgp, 0.0)
        self.assertEqual(self.DUT.n_phases, 1)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.plan_model_id, 0)
        self.assertEqual(self.DUT.prob, 75.0)
        self.assertEqual(self.DUT.producer_risk, 0.0)
        self.assertEqual(self.DUT.scale, 0.0)
        self.assertEqual(self.DUT.scale_ll, 0.0)
        self.assertEqual(self.DUT.scale_se, 0.0)
        self.assertEqual(self.DUT.scale_ul, 0.0)
        self.assertEqual(self.DUT.shape, 0.0)
        self.assertEqual(self.DUT.shape_ll, 0.0)
        self.assertEqual(self.DUT.shape_se, 0.0)
        self.assertEqual(self.DUT.shape_ul, 0.0)
        self.assertEqual(self.DUT.tr, 0.0)
        self.assertEqual(self.DUT.ttt, 0.0)
        self.assertEqual(self.DUT.ttff, 0.0)
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKTest) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKTest) set_attributes should return a zero error code on success
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKTest {0:d} " \
                               "attributes.".format(self.DUT.test_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKTest) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'None', 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKTest " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKTest) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKTest.set_attributes().")
