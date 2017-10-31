#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSoftwareReview.py is part of The RTK
#       Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSoftwareReview module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSoftwareReview import RTKSoftwareReview

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSoftwareReview(unittest.TestCase):
    """
    Class for testing the RTKSoftwareReview class.
    """

    _attributes =(1, 1, 0, 0, 'Test Software Review Type')

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftwareReview class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSoftwareReview).first()
        self.DUT.review_type = self._attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtksoftware_create(self):
        """
        (TestRTKSoftwareReview) __init__ should create an RTKSoftwareReview model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftwareReview))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software_review')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)
        self.assertEqual(self.DUT.review_type, 'Test Software Review Type')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSoftwareReview) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSoftwareReview) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0, 'Test Software Review Type')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating " \
                               "RTKSoftwareReview {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSoftwareReview) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('zero', 0, 'Test Software Review Type')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more " \
                               "RTKSoftwareReview attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSoftwareReview) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKSoftwareReview.set_attributes().")
