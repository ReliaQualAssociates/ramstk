#!/usr/bin/env python -O
"""
This is the test class for testing the Control class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestControl.py is part of The RTK Project
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

from analyses.fmea.Control import Model, Control

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestControlModel(unittest.TestCase):
    """
    Class for testing the Control model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_control_create(self):
        """
        (TestControl) __init__ should return instance of Control data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.cause_id, 0)
        self.assertEqual(self.DUT.control_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.control_type, 0)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestControl) set_attributes should return 0 with good inputs
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2, 3, 'Test Control', 1))
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestControl) set_attributes should return 40 with missing input(s)
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2))
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestControl) set_attributes should return 10 with wrong data type
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, None, 'Test Cause'))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestControl) set_attributes should return 10 with bad value
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 'Test Cause', 2))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestControl) get_attributes should return good values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, 0, '', 0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestControl) get_attributes(set_attributes(values)) == values
        """

        values = (4, 10, 246, 187, 'Test Cause', 1)

        self.DUT.set_attributes(values)
        result = self.DUT.get_attributes()
        self.assertEqual(result, values)


class TestControlController(unittest.TestCase):
    """
    Class for testing the FMEA Control data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control model class.
        """

        self.DUT = Control()

    @attr(all=True, unit=True)
    def test_control_create(self):
        """
        (TestControl) __init__ should return instance of Control data controller
        """

        self.assertTrue(isinstance(self.DUT, Control))
