#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSoftwareDevelopment.py is part of The RTK
#       Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSoftwareDevelopment module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSoftwareDevelopment import RTKSoftwareDevelopment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSoftwareDevelopment(unittest.TestCase):
    """
    Class for testing the RTKSoftwareDevelopment class.
    """

    _attributes =(1, 1, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftwareDevelopment class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSoftwareDevelopment).first()

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtksoftware_create(self):
        """
        (TestRTKSoftwareDevelopment) __init__ should create an RTKSoftwareDevelopment model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftwareDevelopment))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software_development')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSoftwareDevelopment) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSoftwareDevelopment) set_attributes should return a zero error code on success
        """

        _attributes = (0, )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating " \
                               "RTKSoftwareDevelopment {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSoftwareDevelopment) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('one', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more " \
                               "RTKSoftwareDevelopment attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSoftwareDevelopment) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKSoftwareDevelopment.set_attributes().")
