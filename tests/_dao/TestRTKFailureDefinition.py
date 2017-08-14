#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKFailureDefinition.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKFailureDefinition module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKFailureDefinition import RTKFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class Test05RTKFailureDefinition(unittest.TestCase):
    """
    Class for testing the RTKFailureDefinition class.
    """

    _attributes = (1, 1, 'Test Failure Definition')

    def setUp(self):
        """
        Sets up the test fixture for the RTKFailureDefinition class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKFailureDefinition).first()
        self.DUT.definition = self._attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkfailuredefinition_create(self):
        """
        (TestRTKFailureDefinition) __init__ should create an RTKFailureDefinition model.
        """

        self.assertTrue(isinstance(self.DUT, RTKFailureDefinition))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_failure_definition')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.definition_id, 1)
        self.assertEqual(self.DUT.definition, 'Test Failure Definition')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKFailureDefinition) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 1, 'Test Failure Definition'))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a zero error code on success
        """

        _attributes = ('Failure Def.')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFailureDefinition " \
                               "{0:d} attributes.".\
                               format(self.DUT.definition_id))

    @attr(all=True, unit=False)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = [None]

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKEFailureDefinition " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKFailureDefinition.set_attributes().")
