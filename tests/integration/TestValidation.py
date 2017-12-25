#!/usr/bin/env python -O
"""
This is the test class for testing Validation module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestValidation.py is part of The RTK Project
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

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from validation.Validation import Validation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestValidationController(unittest.TestCase):
    """
    Class for testing the Validation data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Validation class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Validation()

    @attr(all=True, integration=True)
    def test_request_tasks(self):
        """
        (TestValidation) request_tasks should return 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_add_task(self):
        """
        (TestValidation) add_task should return 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        self.assertEqual(self.DUT.add_task(0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_task(self):
        """
        (TestValidation) delete_task returns 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        (_results, _error_code) = self.DUT.delete_task(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_task(self):
        """
        (TestValidation) save_task returns 0 on success
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0, 0.0,
                   0.0, 719163, 738163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 90.0)

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        _task = self.DUT.dicTasks[min(self.DUT.dicTasks.keys())]
        _task.set_attributes(_values)

        (_results, _error_code) = self.DUT.save_task(
            min(self.DUT.dicTasks.keys()))

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_tasks(self):
        """
        (TestValidation) save_all_tasks returns 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        self.assertFalse(self.DUT.save_all_tasks())
