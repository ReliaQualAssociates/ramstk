#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKCondition.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the RTKCondition module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKCondition import RTKCondition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKCondition(unittest.TestCase):
    """
    Class for testing the RTKCondition class.
    """

    attributes = (1, 'Cavitation', 'operating')

    def setUp(self):
        """
        Sets up the test fixture for the RTKCondition class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKCondition).first()
        self.DUT.description = self.attributes[1]
        self.DUT.cond_type = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKCondition_create(self):
        """
        (TestRTKCondition) __init__ should create an RTKCondition model
        """

        self.assertTrue(isinstance(self.DUT, RTKCondition))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_condition')
        self.assertEqual(self.DUT.condition_id, 1)
        self.assertEqual(self.DUT.description, 'Cavitation')
        self.assertEqual(self.DUT.cond_type, 'operating')

    @attr(all=True, unit=True)
    def test01_RTKCondition_get_attributes(self):
        """
        (TestRTKCondition) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKCondition_set_attributes(self):
        """
        (TestRTKCondition) set_attributes should return a zero error code on success
        """

        _attributes = ('Vibration', 'operating')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKCondition {0:d} " \
                               "attributes.".format(self.DUT.condition_id))

    @attr(all=True, unit=True)
    def test02b_RTKCondition_set_attributes_to_few(self):
        """
        (TestRTKCondition) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Vibration', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKCondition.set_attributes().")
