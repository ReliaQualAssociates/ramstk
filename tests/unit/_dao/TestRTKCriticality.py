#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKCriticality.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKCriticality module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKCriticality import RTKCriticality

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKCriticality(unittest.TestCase):
    """
    Class for testing the RTKCriticality class.
    """

    attributes = (1, 'Catastrophic',
                  'Could result in death, permanent total disability, loss ' \
                  'exceeding $1M, or irreversible severe environmental ' \
                  'damage that violates law or regulation.', 'I', 4)

    def setUp(self):
        """
        Sets up the test fixture for the RTKCriticality class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        self.DUT = self.dao.session.query(RTKCriticality).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.category = self.attributes[3]
        self.DUT.value = self.attributes[4]

        self.dao.db_update()

    @attr(all=True, unit=True)
    def test00_RTKCriticality_create(self):
        """
        (TestRTKCriticality) __init__ should create an RTKCriticality model
        """

        self.assertTrue(isinstance(self.DUT, RTKCriticality))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_criticality')
        self.assertEqual(self.DUT.criticality_id, 1)
        self.assertEqual(self.DUT.description,
                         'Could result in death, permanent total disability, '\
                         'loss exceeding $1M, or irreversible severe ' \
                         'environmental damage that violates law or ' \
                         'regulation.')
        self.assertEqual(self.DUT.name, 'Catastrophic')
        self.assertEqual(self.DUT.category, 'I')
        self.assertEqual(self.DUT.value, 4)

    @attr(all=True, unit=True)
    def test01_RTKCriticality_get_attributes(self):
        """
        (TestRTKCriticality) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKCriticality_set_attributes(self):
        """
        (TestRTKCriticality) set_attributes should return a zero error code on success
        """

        _attributes = ('Critical',
                       'Could result in permanent partial disability, ' \
                       'injuries or occupational illness that may result in ' \
                       'hospitalization of at least three personnel, loss ' \
                       'exceeding $200K but less than $1M, or reversible ' \
                       'environmental damage causing a violation of law or ' \
                       'regulation.', 'II', 3)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKCriticality {0:d} " \
                               "attributes.".format(self.DUT.criticality_id))

    @attr(all=True, unit=True)
    def test02b_RTKCriticality_set_attributes_to_few(self):
        """
        (TestRTKCriticality) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Critical',
                       'Could result in permanent partial disability, ' \
                       'injuries or occupational illness that may result in ' \
                       'hospitalization of at least three personnel, loss ' \
                       'exceeding $200K but less than $1M, or reversible ' \
                       'environmental damage causing a violation of law or ' \
                       'regulation.', 3)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKCriticality.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RTKCriticality_set_attributes_wrong_type(self):
        """
        (TestRTKCriticality) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Critical',
                       'Could result in permanent partial disability, ' \
                       'injuries or occupational illness that may result in ' \
                       'hospitalization of at least three personnel, loss ' \
                       'exceeding $200K but less than $1M, or reversible ' \
                       'environmental damage causing a violation of law or ' \
                       'regulation.', 3, 'II')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKCriticality " \
                               "attributes.")