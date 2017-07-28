#!/usr/bin/env python -O
"""
This is the test class for testing Assembly module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestAssembly.py is part of The RTK Project
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

import dao.DAO as _dao
from hardware.assembly.Assembly import Model, Assembly

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestAssemblyModel(unittest.TestCase):
    """
    Class for testing the Assembly data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Assembly class.
        """

        _database = '/tmp/tempdb.rtk'

        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestAssembly) __init__ should return an Assembly model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Properly sources the Hardware class.
        self.assertEqual(self.DUT.revision_id, None)

        # Dictionaries are empty.
        self.assertEqual(self.DUT.dicAssemblies, {})
        self.assertEqual(self.DUT.dicComponents, {})

        # Scalar values are correct.
        self.assertEqual(self.DUT.cost_type, 0)
        self.assertEqual(self.DUT.repairable, 1)
        self.assertEqual(self.DUT.total_part_quantity, 0)
        self.assertEqual(self.DUT.total_power_dissipation, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestAssembly) _set_attributes should return a 0 error code on success
        """

        _all_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                       100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                       'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                       'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                       30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 1, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestAssembly) _set_attributes should return a 10 error code when passed a wrong data type
        """

        _all_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                       100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                       'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                       'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                       30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 1, 0, None)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestAssembly) _set_attributes should return a 40 error code when passed too few inputs
        """

        _all_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                       100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                       'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                       'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                       30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                       0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 1, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestAssembly) get_attributes should return a tuple of attribute values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0, 0, 1, 0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _all_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestAssembly) get_attributes(set_attributes(values)) == values
        """

        _all_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0,
                       0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1,
                       '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0, 0, 1, 0, 0.0)

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _all_values)


class TestAssemblyController(unittest.TestCase):
    """
    Class for testing the Assembly data controller class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Component class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Assembly()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestAssembly) __init__ should return an Assembly controller
        """

        self.assertTrue(isinstance(self.DUT, Assembly))
