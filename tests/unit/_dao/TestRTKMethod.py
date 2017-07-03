#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMethod.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKMethod module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKMethod import RTKMethod

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMethod(unittest.TestCase):
    """
    Class for testing the RTKMethod class.
    """

    attributes = (1, 'Code Review',
                  'Code review is a systematic examination (often known as ' \
                  'peer review) of computer source code.',
                  'test')

    def setUp(self):
        """
        Sets up the test fixture for the RTKMethod class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        self.DUT = self.dao.session.query(RTKMethod).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.type = self.attributes[3]

        self.dao.db_update()

    @attr(all=True, unit=True)
    def test00_RTKMethod_create(self):
        """
        (TestRTKMethod) __init__ should create an RTKMethod model
        """

        self.assertTrue(isinstance(self.DUT, RTKMethod))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_method')
        self.assertEqual(self.DUT.method_id, 1)
        self.assertEqual(self.DUT.description,
                         'Code review is a systematic examination (often ' \
                         'known as peer review) of computer source code.')
        self.assertEqual(self.DUT.name, 'Code Review')
        self.assertEqual(self.DUT.type, 'test')

    @attr(all=True, unit=True)
    def test01_RTKMethod_get_attributes(self):
        """
        (TestRTKMethod) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKMethod_set_attributes(self):
        """
        (TestRTKMethod) set_attributes should return a zero error code on success
        """

        _attributes = ('Error/Anomaly Detection', '', 'test')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMethod {0:d} " \
                               "attributes.".format(self.DUT.method_id))

    @attr(all=True, unit=True)
    def test02b_RTKMethods_set_attributes_to_few(self):
        """
        (TestRTKMethod) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Error/Anomaly Detection', '',)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKMethod.set_attributes().")