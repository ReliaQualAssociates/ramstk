#!/usr/bin/env python -O
"""
This is the test class for testing Function module algorithms and models.
"""

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
from revision.Revision import Revision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


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
        self.DUT.dao = self._dao

        self.dtcRevision = Revision()
        self.dtcRevision.dao = self._dao

    @attr(all=True, integration=True)
    def test00_request_functions(self):
        """
        (TestFunction) request_functions should return 0 on success
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)
    # TODO: Test that method fails when no Functions exist in database.
    @attr(all=True, integration=True)
    def test01_add_function(self):
        """
        (TestFunction) add_function returns 0 on success and new Function data model added to dictionary
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)

        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', 'Test Function',
                                               'This is a test function')

        self.assertTrue(isinstance(self.DUT.dicFunctions[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_function_id, 11)

    @attr(all=True, integration=True)
    def test02_add_function_no_parent(self):
        """
        (TestFunction) add_function uses default parent ID when none is passed
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, None, 'F-T', 'New Function',
                                               'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].parent_id,
                         -1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=False)
    def test03_add_function_no_code(self):
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

    @attr(all=True, integration=True)
    def test04_add_function_no_name(self):
        """
        (TestFunction) add_function uses default name when none is passed
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', None,
                                               'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].name,
                         'New Function')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test05_add_function_no_remarks(self):
        """
        (TestFunction) add_function uses default remarks when none is passed
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)
        (_results,
         _error_code,
         _function_id) = self.DUT.add_function(0, 0, 'F-T', 'New Function',
                                               '')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].remarks,
                         '')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test06_delete_function(self):
        """
        (TestFunction) delete_function should return (True, [0, 0]) on success
        """

        self.assertEqual(self.DUT.request_functions(0)[1], 0)
        (_results,
         _error_codes) = self.DUT.delete_function(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_codes, [0, 0])

    @attr(all=True, integration=True)
    def test07_save_function(self):
        """
        (TestFunction) save_function should return (True, 0) on success
        """

        self.DUT.request_functions(0)
        (_results,
         _error_code) = self.DUT.save_function(0)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test08_save_all_functions(self):
        """
        (TestFunction) save_all_functions should return a list of tuples
        """

        self.DUT.request_functions(0)
        self.assertEqual(self.DUT.save_all_functions(),
                         [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                          (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0),
                          (12, 0), (13, 0)])

    @attr(all=True, integration=True)
    def test09_copy_function(self):
        """
        (TestFunction) copy_function should return a dict
        """

        (_results,
         _error_code,
         _revision_id) = self.dtcRevision.add_revision('01', 'New Revision', '')
        self.DUT.request_functions(0)
        _dic_f_xref = self.DUT.copy_function(_revision_id)

        self.assertEqual(_dic_f_xref,
                         {0: 14, 1: 15, 2: 16, 3: 17, 4: 18, 5: 19, 6: 20,
                          7: 21, 8: 22, 9: 23, 10: 24, 11: 25, 12: 26,
                          13: 27, -1: -1})

    @attr(all=True, integration=True)
    def test09a_copy_function_no_revision(self):
        """
        (TestFunction) copy_function should return an empty dict when attempting to copy to a non-existent Revision
        """

        _dic_f_xref = self.DUT.copy_function(2)

        self.assertEqual(_dic_f_xref, {-1:-1})
