#!/usr/bin/env python -O
"""
This is the test class for testing Requirement module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestRequirement.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")
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
    def test_requirement_create(self):
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
    def test_requirement_set_attributes(self):
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
    def test_requirement_set_attributes_wrong_type(self):
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
    def test_requirement_set_attributes_missing_index(self):
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
    def test_requirement_get_attributes(self):
        """
        (TestRequirement) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, '', '', '', 1, '', '', '', 0, '', 0,
                          719163, -1))

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
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
    def test_pack_values(self):
        """
        (TestRequirement) pack_values should return a string with the same integers as the passed list
        """

        _values = [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        self.assertEqual(self.DUT.pack_values(_values), '0111001011001')

    @attr(all=True, unit=True)
    def test_unpack_values(self):

        """
        (TestRequirement) unpack_values should return a list of integers the same as the passed string
        """

        _list = '0111001011001'
        self.assertEqual(self.DUT.unpack_values(_list),
                         [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1])

    @attr(all=True, unit=True)
    def test_pack_unpack_sanity(self):
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
    def test_controller_create(self):
        """
        (TestRequirement) __init__ should create a Requirement data controller
        """

        self.assertTrue(isinstance(self.DUT, Requirement))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicRequirements, {})
