#!/usr/bin/env python -O
"""
This is the test class for testing Requirement module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestRequirement.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from requirement.Requirement import Model, Requirement


class TestRequirementModel(unittest.TestCase):
    """
    Class for testing the Requirement data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Requirement class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

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
        self.assertEqual(self.DUT.code, '')
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
    def test_sanity(self):
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
    def test_pack_values(self):
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

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

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

    @attr(all=True, integration=True)
    def test_request_requirements(self):
        """
        (TestRequirement) request_requirements should return 0 on success
        """

        self.assertEqual(self.DUT.request_requirements(self._dao, 0)[1], 0)
# TODO: Test that method fails when no Requirements exist in database.
    @attr(all=True, integration=True)
    def test_add_requirement(self):
        """
        (TestRequirement) add_requirement returns 0 on success and new Requirement data model added to dictionary
        """

        self.assertEqual(self.DUT.request_requirements(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.add_requirement(0, 0)

        self.assertTrue(isinstance(self.DUT.dicRequirements[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_requirement_no_parent(self):
        """
        (TestRequirement) add_requirement uses default parent ID when none is passed
        """

        self.assertEqual(self.DUT.request_requirements(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.add_requirement(0)
        self.assertEqual(self.DUT.dicRequirements[self.DUT._last_id].parent_id,
                         -1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_requirement(self):
        """
        (TestRequirement) delete_requirement returns 0 on success
        """

        self.assertEqual(self.DUT.request_requirements(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_requirement(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_requirement(self):
        """
        (TestRequirement) save_requirement returns (True, 0) on success
        """

        self.DUT.request_requirements(self._dao, 0)
        self.assertEqual(self.DUT.save_requirement(1), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_requirements(self):
        """
        (TestRequirement) save_all_requirements returns False on success
        """

        self.DUT.request_requirements(self._dao, 0)
        self.assertFalse(self.DUT.save_all_requirements())
