#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRTKCause.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKCause module algorithms and models."""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKCause import RTKCause
from Utilities import OutOfRangeError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKCause(unittest.TestCase):
    """
    Class for testing the RTKCause class.
    """

    _attributes = {
        'rpn_new': 0,
        'rpn_occurrence_new': 0,
        'cause_id': 1,
        'description': 'Test Failure Cause #1',
        'rpn_occurrence': 0,
        'rpn_detection_new': 0,
        'rpn_detection': 0,
        'mechanism_id': 1,
        'rpn': 0
    }

    def setUp(self):
        """Set up the test fixture for the RTKCause class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKCause).first()
        self.DUT.description = self._attributes['description']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkcause_create(self):
        """(TestRTKCause) DUT should create an RTKCause model."""
        self.assertTrue(isinstance(self.DUT, RTKCause))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_cause')
        self.assertEqual(self.DUT.cause_id, 1)
        self.assertEqual(self.DUT.description, 'Test Failure Cause #1')
        self.assertEqual(self.DUT.rpn, 0)
        self.assertEqual(self.DUT.rpn_detection, 0)
        self.assertEqual(self.DUT.rpn_detection_new, 0)
        self.assertEqual(self.DUT.rpn_new, 0)
        self.assertEqual(self.DUT.rpn_occurrence, 0)
        self.assertEqual(self.DUT.rpn_occurrence_new, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKCause) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKCause) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKCause {0:d} " \
                               "attributes.".format(self.DUT.cause_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKCause) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('description')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'description' "
                               "in attribute dictionary passed to "
                               "RTKCause.set_attributes().")

        self._attributes['description'] = 'Test Failure Cause #1'

    @attr(all=True, unit=True)
    def test03b_calculate_rpn_out_of_range_severity_inputs(self):
        """(TestRTKCause) calculate_rpn() raises OutOfRangeError for 11 < severity inputs < 0."""
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 0, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 11, 1)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 0)
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 11)

    @attr(all=True, unit=True)
    def test03c_calculate_rpn_out_of_range_occurrence_inputs(self):
        """(TestRTKCause) calculate_rpn() raises OutOfRangeError for 11 < occurrence inputs < 0."""
        self.DUT.rpn_occurrence = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1)
        self.DUT.rpn_occurrence = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1)

    @attr(all=True, unit=True)
    def test03d_calculate_rpn_out_of_range_new_occurrence_inputs(self):
        """(TestRTKCause) calculate_rpn() raises OutOfRangeError for 11 < new occurrence inputs < 0."""
        self.DUT.rpn_occurrence_new = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1)
        self.DUT.rpn_occurrence_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 1)

    @attr(all=True, unit=True)
    def test03e_calculate_rpn_out_of_range_detection_inputs(self):
        """(TestRTKCause) calculate_rpn() raises OutOfRangeError for 11 < detection inputs < 0."""
        self.DUT.rpn_detection = 0
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 10)
        self.DUT.rpn_detection = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 10)

    @attr(all=True, unit=True)
    def test03f_calculate_rpn_out_of_range_new_detection_inputs(self):
        """(TestRTKCause) calculate_rpn raises OutOfRangeError for 11 < new detection inputs < 0."""
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 10)
        self.DUT.rpn_detection_new = 11
        self.assertRaises(OutOfRangeError, self.DUT.calculate_rpn, 1, 10)
