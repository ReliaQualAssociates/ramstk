#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKFailureMode.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the RTKFailureMode module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKFailureMode import RTKFailureMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKFailureMode(unittest.TestCase):
    """
    Class for testing the RTKFailureMode class.
    """

    attributes = (1, 1, 1, 'Improper Output', 0.77, 2)

    def setUp(self):
        """
        Sets up the test fixture for the RTKFailureMode class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKFailureMode).first()
        self.DUT.description = self.attributes[3]
        self.DUT.mode_ratio = self.attributes[4]
        self.DUT.source = self.attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKFailureMode_create(self):
        """
        (TestRTKFailureMode) __init__ should create an RTKFailureMode model
        """

        self.assertTrue(isinstance(self.DUT, RTKFailureMode))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_failure_mode')
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.subcategory_id, 1)
        self.assertEqual(self.DUT.mode_id, 1)
        self.assertEqual(self.DUT.description, 'Improper Output')
        self.assertEqual(self.DUT.mode_ratio, 0.77)
        self.assertEqual(self.DUT.source, 2)

    @attr(all=True, unit=True)
    def test01_RTKFailureMode_get_attributes(self):
        """
        (TestRTKFailureMode) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKFailureMode_set_attributes(self):
        """
        (TestRTKFailureMode) set_attributes should return a zero error code on success
        """

        _attributes = ('No Output', 0.23, 2)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFailureMode {0:d} " \
                               "attributes.".format(self.DUT.mode_id))

    @attr(all=True, unit=True)
    def test02b_RTKFailureMode_set_attributes_to_few(self):
        """
        (TestRTKFailureMode) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('No Output', 0.23)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKFailureMode.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RTKFailureMode_set_attributes_wrong_type(self):
        """
        (TestRTKFailureMode) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('No Output', 0.23, 'two')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKFailureMode " \
                               "attributes.")