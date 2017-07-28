#!/usr/bin/env python -O
"""
This is the test class for testing Failure Definition module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestFailureDefinition.py is part of The RTK Project
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
from failure_definition.FailureDefinition import FailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = FailureDefinition()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test00_request_definitions(self):
        """
        (TestFailureDefinition) request_definitions should return a list of definitions and an error code of 0 on success
        """

        (_results, _error_code) = self.DUT.request_definitions(0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test01_add_definition(self):
        """
        (TestFailureDefinition) add_definition should return
        """

        self.DUT.request_definitions(0)

        (_results, _error_code, _last_id) = self.DUT.add_definition(0)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test02_save_definition(self):
        """
        (TestFailureDefinition) save_definition should return True on success
        """

        self.DUT.request_definitions(0)

        (_results, _error_code) = self.DUT.save_definitions(0)
        self.assertTrue(_results)

    @attr(all=True, integration=True)
    def test03_delete_definition(self):
        """
        (TestFailureDefinition) delete_definition should return a 0 error code on success
        """

        self.DUT.request_definitions(0)

        (_results, _error_code) = self.DUT.delete_definition(0, 1)
        self.assertEqual(_error_code, 0)
