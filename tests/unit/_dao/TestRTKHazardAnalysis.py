#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKHazardAnalysis.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKHazardAnalysis module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKHazardAnalysis import RTKHazardAnalysis

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKHazardAnalysis(unittest.TestCase):
    """
    Class for testing the RTKHazardAnalysis class.
    """

    _attributes = (1, 1, '', '', 'Assembly Effect', 4, 5, 20, '', 4, 5, 4, '',
                   4, 5, 20, '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0,
                   0.0, 0.0, 0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKHazardAnalysis class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKHazardAnalysis).first()
        self.DUT.assembly_effect = self._attributes[4]

        session.commit()

        @attr(all=True, unit=True)
        def test00_rtkhazard_create(self):
            """
            (TestRTKHazardAnalysis) __init__ should create an RTKHazardAnalysis model.
            """

            self.assertTrue(isinstance(self.DUT, RTKHazard))

            # Verify class attributes are properly initialized.
            self.assertEqual(self.DUT.__tablename__, 'rtk_hazard')
            self.assertEqual(self.DUT.hardware_id, 1)
            self.assertEqual(self.DUT.hazard_id, 1)
            self.assertEqual(self.DUT.potential_hazard, '')
            self.assertEqual(self.DUT.potential_cause, '')
            self.assertEqual(self.DUT.assembly_effect, 'Assembly Effect')
            self.assertEqual(self.DUT.assembly_severity_id, 4)
            self.assertEqual(self.DUT.assembly_probability_id, 5)
            self.assertEqual(self.DUT.assembly_hri, 20)
            self.assertEqual(self.DUT.assembly_mitigation, '')
            self.assertEqual(self.DUT.assembly_severity_id_f, 4)
            self.assertEqual(self.DUT.assembly_probability_id_f, 5)
            self.assertEqual(self.DUT.assembly_hri_id_f, 4)
            self.assertEqual(self.DUT.system_effect, '')
            self.assertEqual(self.DUT.system_severity, 4)
            self.assertEqual(self.DUT.system_probability, 5)
            self.assertEqual(self.DUT.system_hri, 20)
            self.assertEqual(self.DUT.system_mitigation, '')
            self.assertEqual(self.DUT.system_severity_f, 4)
            self.assertEqual(self.DUT.system_probability_f, 5)
            self.assertEqual(self.DUT.system_hri_f, 20)
            self.assertEqual(self.DUT.remarks, '')
            self.assertEqual(self.DUT.function_1, '')
            self.assertEqual(self.DUT.function_2, '')
            self.assertEqual(self.DUT.function_3, '')
            self.assertEqual(self.DUT.function_4, '')
            self.assertEqual(self.DUT.function_5, '')
            self.assertEqual(self.DUT.result_1, 0.0)
            self.assertEqual(self.DUT.result_2, 0.0)
            self.assertEqual(self.DUT.result_3, 0.0)
            self.assertEqual(self.DUT.result_4, 0.0)
            self.assertEqual(self.DUT.result_5, 0.0)
            self.assertEqual(self.DUT.user_blob_1, '')
            self.assertEqual(self.DUT.user_blob_2, '')
            self.assertEqual(self.DUT.user_blob_3, '')
            self.assertEqual(self.DUT.user_Float_1, 0.0)
            self.assertEqual(self.DUT.user_Float_2, 0.0)
            self.assertEqual(self.DUT.user_Float_3, 0.0)
            self.assertEqual(self.DUT.user_int_1, 0)
            self.assertEqual(self.DUT.user_int_2, 0)
            self.assertEqual(self.DUT.user_int_3, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKHazardAnalysis) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKHazardAnalysis) set_attributes should return a zero error code on success
        """

        _attributes = ('', '', 'Assembly Effect', 4, 5, 20, '', 4, 5, 4, '', 4,
                       5, 20, '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0,
                       0.0, 0.0, 0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKHazardAnalysis {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKHazardAnalysis) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('', '', 'Assembly Effect', 4, 5, 20, '', 4, 5, 4, '', 4,
                       5, 20, '', 'four', 5, 20, '', '', '', '', '', '', 0.0,
                       0.0, 0.0, 0.0, 0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKHazardAnalysis " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKHazardAnalysis) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('', '', 'Assembly Effect', 4, 5, 20, '', 4, 5, 4, '', 4,
                       5, 20, '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0,
                       0.0, 0.0, 0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKHazardAnalysis.set_attributes().")
