#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKSoftwareReview.py is part of The RAMSTK
#       Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKSoftwareReview module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RAMSTKSoftwareReview import RAMSTKSoftwareReview

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKSoftwareReview(unittest.TestCase):
    """
    Class for testing the RAMSTKSoftwareReview class.
    """

    _attributes = (1, 1, 0, 0, 'Test Software Review Type')

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKSoftwareReview class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKSoftwareReview).first()
        self.DUT.review_type = self._attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstksoftware_create(self):
        """
        (TestRAMSTKSoftwareReview) __init__ should create an RAMSTKSoftwareReview model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKSoftwareReview))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_software_review')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)
        self.assertEqual(self.DUT.review_type, 'Test Software Review Type')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRAMSTKSoftwareReview) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKSoftwareReview) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0, 'Test Software Review Type')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating " \
                               "RAMSTKSoftwareReview {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKSoftwareReview) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('zero', 0, 'Test Software Review Type')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more " \
                               "RAMSTKSoftwareReview attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKSoftwareReview) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RAMSTKSoftwareReview.set_attributes().")
