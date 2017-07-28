#!/usr/bin/env python -O
"""
This is the test class for testing Incident Component module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestIncidentComponent.py is part of The RTK Project
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
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from incident.component.Component import Model, Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentComponentModel(unittest.TestCase):
    """
    Class for testing the Incident Component data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Incident Component class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestIncidentComponent) __init__ should return an Incident Component model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.incident_id, None)
        self.assertEqual(self.DUT.component_id, None)
        self.assertEqual(self.DUT.age_at_incident, 0.0)
        self.assertEqual(self.DUT.failure, 0)
        self.assertEqual(self.DUT.suspension, 0)
        self.assertEqual(self.DUT.cnd_nff, 0)
        self.assertEqual(self.DUT.occ_fault, 0)
        self.assertEqual(self.DUT.initial_installation, 0)
        self.assertEqual(self.DUT.interval_censored, 0)
        self.assertEqual(self.DUT.use_op_time, 0)
        self.assertEqual(self.DUT.use_cal_time, 0)
        self.assertEqual(self.DUT.ttf, 0.0)
        self.assertEqual(self.DUT.mode_type, 0)

    @attr(all=True, unit=True)
    def test01_set_attributes(self):
        """
        (TestIncidentComponent) set_attributes should return a 0 error code on success
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test02_set_attributes_wrong_type(self):
        """
        (TestIncidentComponent) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test03_set_attributes_missing_index(self):
        """
        (TestIncidentComponent) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test04_get_attributes(self):
        """
        (TestIncidentComponent) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0))

    @attr(all=True, unit=True)
    def test05_sanity(self):
        """
        (TestIncidentComponent) get_attributes(set_attributes(values)) == values
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0)

        self.DUT.set_attributes(_values)
        self.assertEqual(self.DUT.get_attributes(), _values)


class TestIncidentComponentController(unittest.TestCase):
    """
    Class for testing the Incident Component data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident Component class.
        """

        self.DUT = Component()

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestIncidentComponent) __init__ should create a Incident Component data controller
        """

        self.assertTrue(isinstance(self.DUT, Component))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicComponents, {})
