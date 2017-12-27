#!/usr/bin/env python -O
"""
This is the test class for testing Hazard module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestHazard.py is part of The RTK Project
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
from analyses.hazard.Hazard import Hazard

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestHazardController(unittest.TestCase):
    """
    Class for testing the Hazard data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Hazard class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Hazard()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test_request_hazard(self):
        """
        (TestHazard) request_hazard should return 0 on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)

    @attr(all=True, integration=True)
    def test_add_hazard(self):
        """
        (TestHazard) add_hazard should return 0 on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)
        self.assertEqual(self.DUT.add_hazard(0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_hazard(self):
        """
        (TestHazard) delete_hazard should return 0 on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)
        (_results, _error_code) = self.DUT.delete_hazard(0, 1)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_calculate_hazard(self):
        """
        (TestHazard) calculate_hazard should return False on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)
        self.assertFalse(self.DUT.calculate_hazard(0, 2))

    @attr(all=True, integration=True)
    def test_save_hazard(self):
        """
        (TestHazard) save_hazard returns (True, 0) on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)
        self.assertEqual(self.DUT.save_hazard(0, 2), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_hazards(self):
        """
        (TestHazard) save_all_hazards returns False on success
        """

        self.assertEqual(self.DUT.request_hazard()[1], 0)
        self.assertEqual(self.DUT.save_all_hazards(), [(0, 3, 0), (0, 0, 0),
                                                       (0, 2, 0)])
