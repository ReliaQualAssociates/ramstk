#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKValidation.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKValidation module algorithms and models."""

import sys
from os.path import dirname

from datetime import date, timedelta

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

# pylint: disable=E0401,wrong-import-position
from dao.RTKValidation import RTKValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKValidation(unittest.TestCase):
    """Class for testing the RTKValidation database table."""

    _attributes = {
        'cost_minimum': 0.0,
        'validation_id': 1,
        'confidence': 95.0,
        'task_specification': u'',
        'date_start': date(2017, 11, 25),
        'acceptable_variance': 0.0,
        'task_type': u'',
        'measurement_unit': u'',
        'cost_average': 0.0,
        'date_end': date(2017, 12, 25),
        'time_maximum': 0.0,
        'description': 'Test Validation',
        'time_variance': 0.0,
        'acceptable_minimum': 0.0,
        'cost_variance': 0.0,
        'time_minimum': 0.0,
        'acceptable_mean': 0.0,
        'time_mean': 0.0,
        'acceptable_maximum': 0.0,
        'status': 0.0,
        'cost_maximum': 0.0,
        'time_average': 0.0,
        'cost_mean': 0.0,
        'revision_id': 1
    }

    def setUp(self):
        """Set up the test fixture for the RTKValidation class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKValidation).first()
        self.DUT.description = self._attributes['description']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkvalidation_create(self):
        """(TestRTKValidation) __init__ should create an RTKValidation model."""
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
        self.assertEqual(self.DUT.measurement_unit, '')
        self.assertEqual(self.DUT.status, 0.0)
        self.assertEqual(self.DUT.task_type, '')
        self.assertEqual(self.DUT.task_specification, '')
        self.assertEqual(self.DUT.time_average, 0.0)
        self.assertEqual(self.DUT.time_maximum, 0.0)
        self.assertEqual(self.DUT.time_mean, 0.0)
        self.assertEqual(self.DUT.time_minimum, 0.0)
        self.assertEqual(self.DUT.time_variance, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKValidation) get_attributes should return a dict of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKValidation) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKValidation {0:d} "
                         "attributes.".format(self.DUT.validation_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKValidation) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('status')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'status' in "
                         "attribute dictionary passed to "
                         "RTKValidation.set_attributes().")

        self._attributes['status'] = 0.0

    @attr(all=True, unit=True)
    def test_calculate_task_time(self):
        """(TestRTKValidation) calculate returns False on successfully calculating tasks times."""
        self.DUT.time_minimum = 25.2
        self.DUT.time_average = 36.8
        self.DUT.time_maximum = 44.1

        self.assertFalse(self.DUT.calculate_task_time())
        self.assertAlmostEqual(self.DUT.time_mean, 36.08333333)
        self.assertAlmostEqual(self.DUT.time_variance, 9.9225)

    @attr(all=True, unit=True)
    def test_calculate_task_cost(self):
        """(TestRTKValidation) calculate returns False on successfully calculating tasks costs."""
        self.DUT.cost_minimum = 252.00
        self.DUT.cost_average = 368.00
        self.DUT.cost_maximum = 441.00
        self.DUT.confidence = 0.95

        self.assertFalse(self.DUT.calculate_task_cost())
        self.assertAlmostEqual(self.DUT.cost_mean, 360.83333333)
        self.assertAlmostEqual(self.DUT.cost_variance, 992.25)
