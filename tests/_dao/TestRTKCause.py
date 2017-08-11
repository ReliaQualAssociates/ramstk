#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKCause.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKCause module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKCause import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKCause(unittest.TestCase):
    """
    Class for testing the RTKCause class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKCause class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKCause).first()
        self.DUT.description = 'Test Cause'

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkcause_create(self):
        """
        ($f) DUT should create an RTKCause model.
        """

        self.assertTrue(isinstance(self.DUT, RTKCause))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_cause')
        self.assertEqual(self.DUT.cause_id, 1)
        self.assertEqual(self.DUT.description, 'Test Cause')
        self.assertEqual(self.DUT.rpn, 0)
        self.assertEqual(self.DUT.rpn_detection, 0)
        self.assertEqual(self.DUT.rpn_detection_new, 0)
        self.assertEqual(self.DUT.rpn_new, 0)
        self.assertEqual(self.DUT.rpn_occurrence, 0)
        self.assertEqual(self.DUT.rpn_occurrence_new, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKCause) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 1, 'Test Cause', 0, 0, 0, 0, 0, 0))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKCause) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Cause', 0, 0, 0, 0, 0, 1)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKCause {0:d} " \
                               "attributes.".format(self.DUT.cause_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKCause) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Test Cause', 0, 0, 0, 0, 0, 'zero')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKCause " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKCause) set_attributes should return a 40 error code when passed too few attributes
        """


        _attributes = ('Test Cause', 0, 0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKCause.set_attributes().")


