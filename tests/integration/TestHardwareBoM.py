#!/usr/bin/env python -O
"""
This is the test class for testing Hardware BoM module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestBoM.py is part of The RTK Project
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

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
import Configuration
from hardware.BoM import BoM

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestBoMController(unittest.TestCase):
    """
    Class for testing the BoM data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the BoM class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = BoM()
        self.DUT.dao = self._dao

        Configuration.RTK_FAILURE_MODES = {1: {1: [(1, u'Improper Output',
                                                    0.77),
                                                   (2, u'No Output', 0.23)],
                                               2: [(1, u'Output Stuck High',
                                                    0.28),
                                                   (2, u'Output Stuck Low',
                                                    0.28),
                                                   (3, u'Input Open', 0.22),
                                                   (4, u'Output Open', 0.22)],
                                               3: [(1, u'Improper Output',
                                                    0.77),
                                                   (2, u'No Output', 0.23)],
                                               4: [(1, u'Improper Output',
                                                    0.77),
                                                   (2, u'No Output', 0.23)],
                                               5: [(1, u'Data Bit Loss', 0.34),
                                                   (2, u'Short', 0.26),
                                                   (3, u'Open', 0.23),
                                                   (4, u'Slow Transfer of Data',
                                                    0.17)]}}

    @attr(all=True, integration=True)
    def test1_request_bom(self):
        """
        (TestBoM) request_bom should return 0 on success
        """

        self.assertEqual(self.DUT.request_bom(0)[1], 0)

    @attr(all=True, integration=True)
    def test2_add_hardware_assembly(self):
        """
        (TestBoM) add_hardware should return 0 on success
        """

        self.assertEqual(self.DUT.request_bom(0)[1], 0)
        self.assertEqual(self.DUT.add_hardware(0, 0, 0)[1], 0)

    @attr(all=True, integration=True)
    def test3_delete_hardware(self):
        """
        (TestBoM) delete_hardware returns 0 on success
        """

        self.assertEqual(self.DUT.request_bom(0)[1], 0)
        self.DUT.add_hardware(0, 0, 0)

        (_results,
         _error_code) = self.DUT.delete_hardware(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test4_save_hardware_item(self):
        """
        (TestBoM) save_hardware_item returns (True, 0) on success
        """

        self.DUT.request_bom(0)
        self.assertEqual(self.DUT.save_hardware_item(0), (True, 0))

    @attr(all=True, integration=True)
    def test5_save_bom(self):
        """
        (TestBoM) save_bom returns False on success
        """

        self.DUT.request_bom(0)
        self.assertFalse(self.DUT.save_bom())

    @attr(all=True, integration=True)
    def test6_add_failure_modes(self):
        """
        (TestBoM) add_failure_modes returns False on success
        """

        self.DUT.request_bom(0)
        self.assertFalse(self.DUT.add_failure_modes(6))
