#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKTestMethod.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKTestMethod module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKTestMethod import RTKTestMethod

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKTestMethod(unittest.TestCase):
    """
    Class for testing the RTKTestMethod class.
    """

    _attributes =(1, 1, 'Test Test Method', '', '')

    def setUp(self):
        """
        Sets up the test fixture for the RTKTestMethod class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKTestMethod).first()
        self.DUT.description = self._attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtktestmethod_create(self):
        """
        (TestRTKTestMethod) __init__ should create an RTKTestMethod model.
        """

        self.assertTrue(isinstance(self.DUT, RTKTestMethod))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_test_method')
        self.assertEqual(self.DUT.stress_id, 1)
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.description, 'Test Test Method')
        self.assertEqual(self.DUT.boundary_conditions, '')
        self.assertEqual(self.DUT.remarks, '')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKTestMethod) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKTestMethod) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Test Method', '', '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKTestMethod {0:d} " \
                               "attributes.".format(self.DUT.test_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_too_few_passed(self):
        """
        (TestRTKTestMethod) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Test Test Method', '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKTestMethod.set_attributes().")
