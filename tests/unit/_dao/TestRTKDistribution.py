#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKDistribution.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKDistribution module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKDistribution import RTKDistribution

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKDistribution(unittest.TestCase):
    """
    Class for testing the RTKDistribution class.
    """

    attributes = (1, 'Constant Probability', 'statistical')

    def setUp(self):
        """
        Sets up the test fixture for the RTKDistribution class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        self.DUT = self.dao.session.query(RTKDistribution).first()
        self.DUT.description = self.attributes[1]
        self.DUT.type = self.attributes[2]

        self.dao.db_update()

    @attr(all=True, unit=True)
    def test00_RTKDistribution_create(self):
        """
        (TestRTKDistribution) __init__ should create an RTKDistribution model
        """

        self.assertTrue(isinstance(self.DUT, RTKDistribution))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_distribution')
        self.assertEqual(self.DUT.distribution_id, 1)
        self.assertEqual(self.DUT.description, 'Constant Probability')
        self.assertEqual(self.DUT.type, 'statistical')

    @attr(all=True, unit=True)
    def test01_RTKDistribution_get_attributes(self):
        """
        (TestRTKDistribution) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKDistribution_set_attributes(self):
        """
        (TestRTKDistribution) set_attributes should return a zero error code on success
        """

        _attributes = ('Exponential', 'statistical')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKDistribution {0:d} " \
                               "attributes.".format(self.DUT.distribution_id))

    @attr(all=True, unit=True)
    def test02b_RTKDistributions_set_attributes_to_few(self):
        """
        (TestRTKDistributions) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Exponential', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKDistribution.set_attributes().")