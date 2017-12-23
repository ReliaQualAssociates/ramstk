#!/usr/bin/env python -O
"""
This is the test class for testing Software BoM module algorithms and models.
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

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from software.BoM import BoM

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

    @attr(all=True, integration=True)
    def test0_request_bom(self):
        """
        (TestBoM) request_bom should return 0 on success
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 1)[1], 0)

    @attr(all=True, integration=True)
    def test1_add_sftwr_csci(self):
        """
        (TestBoM) add_software should return 0 on success when adding a CSCI
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 1)[1], 0)
        self.assertEqual(self.DUT.add_software(0, 1, 0)[1], 0)

    @attr(all=True, integration=True)
    def test2_add_sftwr_unit(self):
        """
        (TestBoM) add_software should return 0 on success when adding a unit
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 1)[1], 0)
        self.assertEqual(self.DUT.add_software(0, 2, 2)[1], 0)

    @attr(all=True, integration=False)
    def test3_delete_software(self):
        """
        (TestBoM) delete_software returns 0 on success
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 1)[1], 0)
        (_results, _error_code) = self.DUT.delete_software(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test4_save_software_item(self):
        """
        (TestBoM) save_software_item returns (True, 0) on success
        """

        self.DUT.request_bom(self._dao, 0)
        self.assertEqual(self.DUT.save_software_item(1), (True, 0))

    @attr(all=True, integration=True)
    def test5_save_development_risk(self):
        """
        (TestBoM) save_development_risk returns (True, 0) on success
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[1].lst_development[2] = 1
        self.DUT.dicSoftware[1].lst_development[12] = 1

        self.assertEqual(self.DUT.save_development_risk(2), (True, 0))

    @attr(all=True, integration=True)
    def test6_save_srr_risk(self):
        """
        (TestBoM) save_srr_risk returns (True, 0) on success
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[1].lst_anomaly_mgmt[0][2] = 1
        self.DUT.dicSoftware[1].lst_anomaly_mgmt[0][12] = 1
        self.DUT.dicSoftware[1].lst_traceability[0][0] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[0][2] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[0][9] = 12

        self.assertEqual(self.DUT.save_srr_risk(1), (True, 0))

    @attr(all=True, integration=True)
    def test7_save_pdr_risk(self):
        """
        (TestBoM) save_pdr_risk returns (True, 0) on success
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[1].lst_anomaly_mgmt[1][2] = 1
        self.DUT.dicSoftware[1].lst_anomaly_mgmt[1][12] = 1
        self.DUT.dicSoftware[1].lst_traceability[1][0] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[1][2] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[1][9] = 12

        self.assertEqual(self.DUT.save_pdr_risk(1), (True, 0))

    @attr(all=True, integration=True)
    def test8_save_cdr_risk_csci(self):
        """
        (TestBoM) save_cdr_risk returns (True, 0) on success when saving CSCI risk
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[1].lst_anomaly_mgmt[2][0] = 10
        self.DUT.dicSoftware[1].lst_anomaly_mgmt[2][2] = 1
        self.DUT.dicSoftware[1].lst_traceability[2][0] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[2][2] = 1
        self.DUT.dicSoftware[1].lst_sftw_quality[2][9] = 12

        self.assertEqual(self.DUT.save_cdr_risk(1), (True, 0))

    @attr(all=True, integration=True)
    def test9_save_cdr_risk_unit(self):
        """
        (TestBoM) save_cdr_risk returns (True, 0) on success when saving Unit risk
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[2].lst_anomaly_mgmt[2][0] = 10
        self.DUT.dicSoftware[2].lst_anomaly_mgmt[2][2] = 1
        self.DUT.dicSoftware[2].lst_traceability[2][0] = 1
        self.DUT.dicSoftware[2].lst_sftw_quality[2][2] = 1
        self.DUT.dicSoftware[2].lst_sftw_quality[2][9] = 12

        self.assertEqual(self.DUT.save_cdr_risk(2), (True, 0))

    @attr(all=True, integration=True)
    def test10_save_trr_risk_csci(self):
        """
        (TestBoM) save_trr_risk returns (True, 0) on success when saving CSCI risk
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[1].lst_modularity[0] = 10
        self.DUT.dicSoftware[1].lst_modularity[1] = 135
        self.DUT.dicSoftware[1].lst_modularity[2] = 12
        self.DUT.dicSoftware[1].lst_modularity[3] = 15

        self.assertEqual(self.DUT.save_trr_risk(1), (True, 0))

    @attr(all=True, integration=True)
    def test11_save_trr_risk_unit(self):
        """
        (TestBoM) save_trr_risk returns (True, 0) on success when saving Unit risk
        """

        self.DUT.request_bom(self._dao, 0)

        self.DUT.dicSoftware[2].lst_modularity[0] = 10
        self.DUT.dicSoftware[2].lst_modularity[1] = 135
        self.DUT.dicSoftware[2].lst_modularity[2] = 12
        self.DUT.dicSoftware[2].lst_anomaly_mgmt[3][0] = 1
        self.DUT.dicSoftware[2].lst_sftw_quality[3][1] = 1
        self.DUT.dicSoftware[2].lst_sftw_quality[3][6] = 1
        self.DUT.dicSoftware[2].lst_sftw_quality[3][12] = 1

        self.assertEqual(self.DUT.save_trr_risk(2), (True, 0))

    @attr(all=True, integration=True)
    def test12_save_bom(self):
        """
        (TestBoM) save_bom returns False on success
        """

        self.DUT.request_bom(self._dao, 0)
        self.assertFalse(self.DUT.save_bom())
