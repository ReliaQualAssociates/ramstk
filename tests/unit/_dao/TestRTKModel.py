#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKModel.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKModel module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKModel import RTKModel

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKModel(unittest.TestCase):
    """
    Class for testing the RTKModel class.
    """

    attributes = (1, 'Equal Apportionment', 'allocation')

    def setUp(self):
        """
        Sets up the test fixture for the RTKModel class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKModel).first()
        self.DUT.description = self.attributes[1]
        self.DUT.type = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKModel_create(self):
        """
        (TestRTKModel) __init__ should create an RTKModel model
        """

        self.assertTrue(isinstance(self.DUT, RTKModel))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_model')
        self.assertEqual(self.DUT.model_id, 1)
        self.assertEqual(self.DUT.description, 'Equal Apportionment')
        self.assertEqual(self.DUT.type, 'allocation')

    @attr(all=True, unit=True)
    def test01_RTKModel_get_attributes(self):
        """
        (TestRTKModel) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKModel_set_attributes(self):
        """
        (TestRTKModel) set_attributes should return a zero error code on success
        """

        _attributes = ('ARINC Apportionment', 'allocation')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKModel {0:d} " \
                               "attributes.".format(self.DUT.model_id))

    @attr(all=True, unit=True)
    def test02b_RTKModel_set_attributes_to_few(self):
        """
        (TestRTKModel) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('ARINC Apportionment',)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKModel.set_attributes().")