#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKRequirement.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKRequirement module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKRequirement import RTKRequirement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class Test06RTKRequirement(unittest.TestCase):
    """
    Class for testing the RTKRequirement class.
    """

    _attributes = (1, 1, 0, 'Test Requirement', '', '', '', 0, 0, 'Test Code',
                   '', '', 0, date.today(),
                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKRequirement class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKRequirement).first()
        self.DUT.description = self._attributes[3]
        self.DUT.requirement_code = self._attributes[9]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkrequirement_create(self):
        """
        (TestRTKRequirement) __init__ should create an RTKRequirement model.
        """

        self.assertTrue(isinstance(self.DUT, RTKRequirement))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_requirement')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.requirement_id, 1)
        self.assertEqual(self.DUT.derived, 0)
        self.assertEqual(self.DUT.description, 'Test Requirement')
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.owner, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.priority, 0)
        self.assertEqual(self.DUT.requirement_code, 'Test Code')
        self.assertEqual(self.DUT.specification, '')
        self.assertEqual(self.DUT.requirement_type, '')
        self.assertEqual(self.DUT.validated, 0)
        self.assertEqual(self.DUT.validated_date, date.today())
        self.assertEqual(self.DUT.q_clarity_0, 0)
        self.assertEqual(self.DUT.q_clarity_1, 0)
        self.assertEqual(self.DUT.q_clarity_2, 0)
        self.assertEqual(self.DUT.q_clarity_3, 0)
        self.assertEqual(self.DUT.q_clarity_4, 0)
        self.assertEqual(self.DUT.q_clarity_5, 0)
        self.assertEqual(self.DUT.q_clarity_6, 0)
        self.assertEqual(self.DUT.q_clarity_7, 0)
        self.assertEqual(self.DUT.q_clarity_8, 0)
        self.assertEqual(self.DUT.q_complete_0, 0)
        self.assertEqual(self.DUT.q_complete_1, 0)
        self.assertEqual(self.DUT.q_complete_2, 0)
        self.assertEqual(self.DUT.q_complete_3, 0)
        self.assertEqual(self.DUT.q_complete_4, 0)
        self.assertEqual(self.DUT.q_complete_5, 0)
        self.assertEqual(self.DUT.q_complete_6, 0)
        self.assertEqual(self.DUT.q_complete_7, 0)
        self.assertEqual(self.DUT.q_complete_8, 0)
        self.assertEqual(self.DUT.q_complete_9, 0)
        self.assertEqual(self.DUT.q_consistent_0, 0)
        self.assertEqual(self.DUT.q_consistent_1, 0)
        self.assertEqual(self.DUT.q_consistent_2, 0)
        self.assertEqual(self.DUT.q_consistent_3, 0)
        self.assertEqual(self.DUT.q_consistent_4, 0)
        self.assertEqual(self.DUT.q_consistent_5, 0)
        self.assertEqual(self.DUT.q_consistent_6, 0)
        self.assertEqual(self.DUT.q_consistent_7, 0)
        self.assertEqual(self.DUT.q_consistent_8, 0)
        self.assertEqual(self.DUT.q_verifiable_0, 0)
        self.assertEqual(self.DUT.q_verifiable_1, 0)
        self.assertEqual(self.DUT.q_verifiable_2, 0)
        self.assertEqual(self.DUT.q_verifiable_3, 0)
        self.assertEqual(self.DUT.q_verifiable_4, 0)
        self.assertEqual(self.DUT.q_verifiable_5, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKRequirement) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKRequirement) set_attributes should return a zero error code on success
        """

        _error_code, _msg = self.DUT.set_attributes(self._attributes[2:])

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRequirement {0:d} " \
                               "attributes.".format(self.DUT.requirement_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKRequirement) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (1, 1, 0, 'Test Requirement', '', '', '', 0, 0,
                       'Test Code', '', '', 0, date.today(),
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       None, 0, 0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKRequirement " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKRequirement) set_attributes() should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 'Test Requirement', '', '', '', 0, 0, 'Test Code',
                       '', '', 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKRequirement.set_attributes().")

    @attr(all=True, unit=True)
    def test03a_create_code(self):
        """
        (TestRTKRequirement) create_code should return False on success.
        """

        self.assertFalse(self.DUT.create_code('PERF'))
        self.assertEqual(self.DUT.requirement_code, 'PERF-0001')
