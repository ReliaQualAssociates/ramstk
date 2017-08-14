#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKValidation.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKValidation module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKValidation import RTKValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKValidation(unittest.TestCase):
    """
    Class for testing the RTKValidation class.
    """

    _attributes =(1, 1, 0.0, 0.0, 0.0, 0.0, 95.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  date.today() + timedelta(days=30), date.today(),
                  'Test Validation', 0, 0.0, 0, '', 0.0, 0.0, 0.0, 0.0, 0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKValidation class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKValidation).first()
        self.DUT.description = self._attributes[14]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkvalidation_create(self):
        """
        (TestRTKValidation) __init__ should create an RTKValidation model.
        """

        self.assertTrue(isinstance(self.DUT, RTKValidation))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_validation')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.validation_id, 1)
        self.assertEqual(self.DUT.acceptable_maximum, 0.0)
        self.assertEqual(self.DUT.acceptable_mean, 0.0)
        self.assertEqual(self.DUT.acceptable_minimum, 0.0)
        self.assertEqual(self.DUT.acceptable_variance, 0.0)
        self.assertEqual(self.DUT.confidence, 95.0)
        self.assertEqual(self.DUT.cost_average, 0.0)
        self.assertEqual(self.DUT.cost_maximum, 0.0)
        self.assertEqual(self.DUT.cost_mean, 0.0)
        self.assertEqual(self.DUT.cost_minimum, 0.0)
        self.assertEqual(self.DUT.cost_variance, 0.0)
        self.assertEqual(self.DUT.date_end, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.date_start, date.today())
        self.assertEqual(self.DUT.description, 'Test Validation')
        self.assertEqual(self.DUT.measurement_unit_id, 0)
        self.assertEqual(self.DUT.status_id, 0.0)
        self.assertEqual(self.DUT.task_type_id, 0)
        self.assertEqual(self.DUT.task_specification, '')
        self.assertEqual(self.DUT.time_average, 0.0)
        self.assertEqual(self.DUT.time_maximum, 0.0)
        self.assertEqual(self.DUT.time_mean, 0.0)
        self.assertEqual(self.DUT.time_minimum, 0.0)
        self.assertEqual(self.DUT.time_variance, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKValidation) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKValidation) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0.0, 0.0, 0.0, 95.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       date.today() + timedelta(days=30), date.today(),
                       'Test Validation', 0, 0.0, 0, '', 0.0, 0.0, 0.0, 0.0,
                       0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKValidation {0:d} " \
                               "attributes.".format(self.DUT.validation_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKValidation) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, None, 0.0, 0.0, 95.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       date.today() + timedelta(days=30), date.today(),
                       'Test Validation', 0, 0.0, 0, '', 0.0, 0.0, 0.0, 0.0,
                       0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKValidation " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKValidation) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0.0, 0.0, 0.0, 95.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       date.today() + timedelta(days=30), date.today(),
                       'Test Validation', 0, 0.0, 0, '', 0.0, 0.0, 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKValidation.set_attributes().")
