#!/usr/bin/env python -O
"""
This is the test class for testing Function module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.integration.TestFunction.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from function.Function import Model, Function


class TestFunctionController(unittest.TestCase):
    """
    Class for testing the Function data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Function class.
        """

        _database = '/tmp/tempdb.rtk'

        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Function()

    @attr(all=True, integration=True)
    def test0_request_functions(self):
        """
        (TestFunction) request_functions should return 0 on success
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
# TODO: Test that method fails when no Functions exist in database.
    @attr(all=True, integration=True)
    def test1_add_function(self):
        """
        (TestFunction) add_function returns 0 on success and new Function data model added to dictionary
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', 'Test Function',
                                               'This is a test function')

        self.assertTrue(isinstance(self.DUT.dicFunctions[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_function_id, 1)

    @attr(all=True, integration=True)
    def test2_add_function_no_parent(self):
        """
        (TestFunction) add_function uses default parent ID when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, None, 'F-T', 'New Function',
                                               'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].parent_id,
                         -1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test3_add_function_no_code(self):
        """
        (TestFunction) add_function uses default code when none is passed
        """
# TODO: This test requires the configuration values to be set.
        #self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        #(_results,
        # _error_code) = self.DUT.add_function(0, 0, None, 'New Function',
        #                                      'This is a test function')
        #self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].name,
        #                 'New Function')
        #self.assertTrue(_results)
        #self.assertEqual(_error_code, 0)

        pass

    @attr(all=True, integration=True)
    def test4_add_function_no_name(self):
        """
        (TestFunction) add_function uses default name when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', None,
                                              'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].name,
                         'New Function')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test5_add_function_no_remarks(self):
        """
        (TestFunction) add_function uses default remarks when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', 'New Function',
                                              '')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].remarks,
                         '')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test6_delete_function(self):
        """
        (TestFunction) delete_function should return (True, [0, 0, 0]) on success
        """

        self.assertEqual(self.DUT.request_functions(self._dao, 0)[1], 0)
        (_results,
         _error_codes) = self.DUT.delete_function(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_codes, [0, 0, 0])

    @attr(all=True, integration=True)
    def test7_save_function(self):
        """
        (TestFunction) save_function should return (True, 0) on success
        """

        self.DUT.request_functions(self._dao, 0)
        (_results,
         _error_code) = self.DUT.save_function(0)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test8_save_all_functions(self):
        """
        (TestFunction) save_all_functions should return a list of tuples
        """

        self.DUT.request_functions(self._dao, 0)
        self.assertEqual(self.DUT.save_all_functions(),
                         [(0, 0), (1, 0), (2, 0), (3, 0)])
