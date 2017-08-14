#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestRequirement.py is part of The RTK Project
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

"""
This is the test class for testing Requirement module algorithms and models.
"""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )
from requirement.Requirement import Model, Requirement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "Weibullguy" Rowland'


class TestRequirementModel(unittest.TestCase):
    """
    Class for testing the Requirement data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Requirement class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test00_requirement_create(self):
        """
        (TestRequirement) __init__ should return a Requirement model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.lst_clear, [])
        self.assertEqual(self.DUT.lst_complete, [])
        self.assertEqual(self.DUT.lst_consistent, [])
        self.assertEqual(self.DUT.lst_verifiable, [])
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.requirement_id, None)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.requirement_code, '')
        self.assertEqual(self.DUT.requirement_type, '')
        self.assertEqual(self.DUT.priority, 1)
        self.assertEqual(self.DUT.specification, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.derived, 0)
        self.assertEqual(self.DUT.owner, '')
        self.assertEqual(self.DUT.validated, 0)
        self.assertEqual(self.DUT.validated_date, 719163)
        self.assertEqual(self.DUT.parent_id, -1)

    @attr(all=True, unit=True)
    def test01_requirement_set_attributes(self):
        """
        (TestRequirement) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 'Requirement Description', 'Code', 'Functional', 2,
                   'Specification', 'Page #', 'Figure #', 0, 'Me', 1, 729163,
                   -1, '11011', '1010', '11110011', '01101')
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test01a_requirement_set_attributes_wrong_type(self):
        """
        (TestRequirement) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 'Requirement Description', 'Code', 'Functional', None,
                   'Specification', 'Page #', 'Figure #', 0, 'Me', 1, 729163,
                   -1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test02a_requirement_set_attributes_missing_index(self):
        """
        (TestRequirement) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 'Requirement Description', 'Code', 'Functional', 2,
                   'Specification', 'Page #', 'Figure #', 0, 'Me', 729163,
                   -1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test03_requirement_get_attributes(self):
        """
        (TestRequirement) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, '', '', '', 1, '', '', '', 0, '', 0,
                          719163, -1))

    @attr(all=True, unit=True)
    def test04_attribute_sanity(self):
        """
        (TestRequirement) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 'Requirement Description', 'Code', 'Functional', 2,
                   'Specification', 'Page #', 'Figure #', 0, 'Me', 1, 729163,
                   -1)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test05_pack_values(self):
        """
        (TestRequirement) pack_values should return a string with the same integers as the passed list
        """

        _values = [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        self.assertEqual(self.DUT.pack_values(_values), '0111001011001')

    @attr(all=True, unit=True)
    def test06_unpack_values(self):

        """
        (TestRequirement) unpack_values should return a list of integers the same as the passed string
        """

        _list = '0111001011001'
        self.assertEqual(self.DUT.unpack_values(_list),
                         [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1])

    @attr(all=True, unit=True)
    def test07_pack_unpack_sanity(self):
        """
        (TestRequirement) unpack_values(pack_values(values)) == values
        """

        _values = [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        _list = self.DUT.pack_values(_values)
        self.assertEqual(self.DUT.unpack_values(_list), _values)


class TestRequirementController(unittest.TestCase):
    """
    Class for testing the Requirement data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Requirement class.
        """

        self.DUT = Requirement()

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestRequirement) __init__ should create a Requirement data controller
        """

        self.assertTrue(isinstance(self.DUT, Requirement))
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicRequirements, {})
        self.assertEqual(self.DUT.dao, None)
