#!/usr/bin/env python -O
"""
This is the test class for testing Allocation module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.integration.TestAllocation.py is part of The RTK Project
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
from analyses.allocation.Allocation import Allocation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestAllocationController(unittest.TestCase):
    """
    Class for testing the Allocation data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Allocation class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Allocation()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test_request_allocation(self):
        """
        (TestAllocation) request_allocation should return 0 on success
        """

        self.assertEqual(self.DUT.request_allocation()[1], 0)

    @attr(all=True, integration=True)
    def test_allocate_equal(self):
        """
        (TestAllocation) allocate should return False on success when using equal allocation
        """

        self.DUT.request_allocation()
        self.DUT.dicAllocation[0].reliability_goal = 0.975
        self.DUT.dicAllocation[0].method = 1
        self.assertFalse(self.DUT.allocate(0))

    @attr(all=True, integration=True)
    def test_allocate_agree(self):
        """
        (TestAllocation) allocate should return False on success when using AGREE allocation
        """

        self.DUT.request_allocation()
        self.DUT.dicAllocation[0].reliability_goal = 0.975
        self.DUT.dicAllocation[0].method = 2
        self.assertFalse(self.DUT.allocate(0))

    @attr(all=True, integration=True)
    def test_allocate_arinc(self):
        """
        (TestAllocation) allocate should return False on success when using ARINC allocation
        """

        self.DUT.request_allocation()
        self.DUT.dicAllocation[2]._hazard_rate = 0.0005
        self.DUT.dicAllocation[7]._hazard_rate = 0.0002
        self.DUT.dicAllocation[8]._hazard_rate = 0.0003
        self.DUT.dicAllocation[2].reliability_goal = 0.975
        self.DUT.dicAllocation[2].method = 3
        self.assertFalse(self.DUT.allocate(2))

    @attr(all=True, integration=True)
    def test_allocate_foo(self):
        """
        (TestAllocation) allocate should return False on success when using FOO allocation
        """

        self.DUT.request_allocation()
        self.DUT.dicAllocation[2]._hazard_rate = 0.0005
        self.DUT.dicAllocation[7]._hazard_rate = 0.0002
        self.DUT.dicAllocation[8]._hazard_rate = 0.0003
        self.DUT.dicAllocation[2].reliability_goal = 0.975
        self.DUT.dicAllocation[2].method = 4
        self.DUT.dicAllocation[2].int_factor = 3
        self.DUT.dicAllocation[2].soa_factor = 7
        self.DUT.dicAllocation[2].op_time_factor = 10
        self.DUT.dicAllocation[2].env_factor = 4
        self.assertFalse(self.DUT.allocate(2))

    @attr(all=True, integration=True)
    def test_save_allocation(self):
        """
        (TestAllocation) save_allocation returns (True, 0) on success
        """

        self.DUT.request_allocation()
        self.assertEqual(self.DUT.save_allocation(0), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_allocation(self):
        """
        (TestAllocation) save_all_allocation returns False on success
        """

        self.DUT.request_allocation()
        self.assertEqual(self.DUT.save_all_allocation(),
                         [(0, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0),
                          (8, 0), (105, 0), (115, 0), (88, 0), (102, 0)])

    @attr(all=True, integration=True)
    def test_trickle_down(self):
        """
        (TestAllocation) trickle_down should return False on sucess
        """

        self.DUT.request_allocation()
        self.assertFalse(self.DUT.trickle_down(0))
