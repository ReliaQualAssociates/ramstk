#!/usr/bin/env python -O
"""
This is the test class for testing the Cause class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestCause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from analyses.fmea.Cause import Model, Cause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestCauseModel(unittest.TestCase):
    """
    Class for testing the Cause model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Cause model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_cause_create(self):
        """
        __init__ should return instance of Cause data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dicActions, {})
        self.assertEqual(self.DUT.dicControls, {})

        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.cause_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.rpn_occurrence, 9)
        self.assertEqual(self.DUT.rpn_detection, 9)
        self.assertEqual(self.DUT.rpn, 1000)
        self.assertEqual(self.DUT.rpn_occurrence_new, 9)
        self.assertEqual(self.DUT.rpn_detection_new, 9)
        self.assertEqual(self.DUT.rpn_new, 1000)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        set_attributes should return 0 with good inputs
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2, 'Test Cause', 4, 5,
                                                200, 5, 4, 100))
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        set_attributes should return 40 with mission input(s)
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2))
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_good_attributes_wrong_type(self):
        """
        set_attributes should return 10 with wrong data type
        """

        # Check TypeError.
        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, None, 'Test Cause', 4, 5,
                                                200, 5, 4, 100))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_good_attributes_wrong_value(self):
        """
        set_attributes should return 10 with bad value
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 'Test Cause', 2, 4, 5,
                                                200, 5, 4, 100))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        get_attributes should return good values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, '', 9, 9, 1000, 9, 9, 1000))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        get_attributes(set_attributes(values)) == values
        """

        values = (4, 10, 246, 'Test Cause', 4, 5, 200, 5, 4, 100)

        self.DUT.set_attributes(values)
        result = self.DUT.get_attributes()
        self.assertEqual(result, values)


class TestCauseController(unittest.TestCase):
    """
    Class for testing the FMEA Cause data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Cause model class.
        """

        self.DUT = Cause()

    @attr(all=True, unit=True)
    def test_cause_create(self):
        """
        (TestCause) __init__ should return instance of Cause data controller
        """

        self.assertTrue(isinstance(self.DUT, Cause))
