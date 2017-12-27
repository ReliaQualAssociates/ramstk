#!/usr/bin/env python -O
"""
This is the test class for testing software Unit module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.software.TestUnit.py is part of The RTK Project
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

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

from software.Unit import Model
from software.Software import _calculate_anomaly_risk, _calculate_quality_risk

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestUnitModel(unittest.TestCase):
    """
    Class for testing the Unit data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Unit class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestSoftware) __init__ should return a Unit model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.software_id, None)
        self.assertEqual(self.DUT.level_id, 3)
        self.assertEqual(self.DUT.description, "")
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.development_id, 0)
        self.assertEqual(self.DUT.a_risk, 0.0)
        self.assertEqual(self.DUT.do, 0.0)
        self.assertEqual(self.DUT.dd, 0)
        self.assertEqual(self.DUT.dc, 0.0)
        self.assertEqual(self.DUT.d_risk, 0.0)
        self.assertEqual(self.DUT.am, 0.0)
        self.assertEqual(self.DUT.sa, 0.0)
        self.assertEqual(self.DUT.st, 0.0)
        self.assertEqual(self.DUT.dr, 0.0)
        self.assertEqual(self.DUT.sq, 0.0)
        self.assertEqual(self.DUT.s1, 0.0)
        self.assertEqual(self.DUT.hloc, 0)
        self.assertEqual(self.DUT.aloc, 0)
        self.assertEqual(self.DUT.sloc, 0)
        self.assertEqual(self.DUT.sl, 0.0)
        self.assertEqual(self.DUT.ax, 0)
        self.assertEqual(self.DUT.bx, 0)
        self.assertEqual(self.DUT.cx, 0)
        self.assertEqual(self.DUT.nm, 0)
        self.assertEqual(self.DUT.sx, 0.0)
        self.assertEqual(self.DUT.um, 0)
        self.assertEqual(self.DUT.wm, 0)
        self.assertEqual(self.DUT.xm, 0)
        self.assertEqual(self.DUT.sm, 1.0)
        self.assertEqual(self.DUT.df, 0.0)
        self.assertEqual(self.DUT.sr, 0.0)
        self.assertEqual(self.DUT.s2, 0.0)
        self.assertEqual(self.DUT.rpfom, 0.0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.dev_assess_type, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.tcl, 0)
        self.assertEqual(self.DUT.test_path, 0)
        self.assertEqual(self.DUT.category, 0)
        self.assertEqual(self.DUT.test_effort, 0)
        self.assertEqual(self.DUT.test_approach, 0)
        self.assertEqual(self.DUT.labor_hours_test, 0.0)
        self.assertEqual(self.DUT.labor_hours_dev, 0.0)
        self.assertEqual(self.DUT.budget_test, 0.0)
        self.assertEqual(self.DUT.budget_dev, 0.0)
        self.assertEqual(self.DUT.schedule_test, 0.0)
        self.assertEqual(self.DUT.schedule_dev, 0.0)
        self.assertEqual(self.DUT.branches, 0)
        self.assertEqual(self.DUT.branches_test, 0)
        self.assertEqual(self.DUT.inputs, 0)
        self.assertEqual(self.DUT.inputs_test, 0)
        self.assertEqual(self.DUT.nm_test, 0)
        self.assertEqual(self.DUT.interfaces, 0)
        self.assertEqual(self.DUT.interfaces_test, 0)
        self.assertEqual(self.DUT.te, 0.0)
        self.assertEqual(self.DUT.tm, 0.0)
        self.assertEqual(self.DUT.tc, 0.0)
        self.assertEqual(self.DUT.t_risk, 0.0)
        self.assertEqual(self.DUT.ft1, 0.0)
        self.assertEqual(self.DUT.ft2, 0.0)
        self.assertEqual(self.DUT.ren_avg, 0.0)
        self.assertEqual(self.DUT.ren_eot, 0.0)
        self.assertEqual(self.DUT.ec, 0.0)
        self.assertEqual(self.DUT.ev, 0.0)
        self.assertEqual(self.DUT.et, 0.0)
        self.assertEqual(self.DUT.os, 0.0)
        self.assertEqual(self.DUT.ew, 0.0)
        self.assertEqual(self.DUT.e_risk, 0.0)
        self.assertEqual(self.DUT.failure_rate, 0.0)
        self.assertEqual(self.DUT.units, 0)
        self.assertEqual(self.DUT.units_test, 0)

    @attr(all=True, unit=True)
    def test01_calculate_anomaly_risk(self):
        """
        (TestSoftware) _calculate_anomaly_risk should return False on success
        """

        self.DUT.phase_id = 3  # CDR
        self.DUT.lst_anomaly_mgmt = [[], [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0
        ]]

        _error_code = _calculate_anomaly_risk(self.DUT)
        self.assertEqual(_error_code, 0)
        self.assertAlmostEqual(self.DUT.am, 0.1428571)
        self.assertEqual(self.DUT.sa, 0.9)

    @attr(all=True, unit=True)
    def test02_calculate_quality_risk(self):
        """
        (TestSoftware) _calculate_quality_risk should return a 0 error code on success
        """

        self.DUT.phase_id = 3  # PDR
        self.DUT.lst_sftw_quality = [[], [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0
        ]]

        _error_code = _calculate_quality_risk(self.DUT)
        self.assertEqual(_error_code, 0)
        self.assertAlmostEqual(self.DUT.dr, 0.4736842)
        self.assertAlmostEqual(self.DUT.sq, 1.1)
