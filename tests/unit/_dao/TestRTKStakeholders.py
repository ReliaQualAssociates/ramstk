#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKStakeholders.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKStakeholders module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKStakeholders import RTKStakeholders

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKStakeholders(unittest.TestCase):
    """
    Class for testing the RTKStakeholders class.
    """

    attributes = (1, 'Customer')

    def setUp(self):
        """
        Sets up the test fixture for the RTKStakeholders class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        self.DUT = self.dao.session.query(RTKStakeholders).first()
        self.DUT.stakeholder = self.attributes[1]

        self.dao.db_update()

    @attr(all=True, unit=True)
    def test00_RTKStakeholders_create(self):
        """
        (TestRTKStakeholders) __init__ should create an RTKStakeholders model
        """

        self.assertTrue(isinstance(self.DUT, RTKStakeholders))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_stakeholders')
        self.assertEqual(self.DUT.stakeholders_id, 1)
        self.assertEqual(self.DUT.stakeholder, 'Customer')

    @attr(all=True, unit=True)
    def test01_RTKStakeholders_get_attributes(self):
        """
        (TestRTKStakeholders) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKStakeholders_set_attributes(self):
        """
        (TestRTKStakeholders) set_attributes should return a zero error code on success
        """

        _attributes = ('Marketing', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKStakeholders {0:d} " \
                               "attributes.".format(self.DUT.stakeholders_id))

    @attr(all=True, unit=True)
    def test02b_RTKStakeholders_set_attributes_to_few(self):
        """
        (TestRTKStakeholders) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKStakeholders.set_attributes().")
