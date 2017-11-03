#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.integration.TestRequirement.py is part of The RTK Project
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

"""
This is the test class for testing Requirement module algorithms and models.
"""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )
import dao.DAO as _dao
from requirement.Requirement import Model, Requirement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestRequirementController(unittest.TestCase):
    """
    Class for testing the Requirement data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Requirement class.
        """

        _database = '/tmp/tempdb.rtk'

        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Requirement()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test00_request_requirements(self):
        """
        (TestRequirement) request_requirements should return 0 on success
        """

        self.assertEqual(self.DUT.request_requirements(0)[1], 0)
    # TODO: Test that method fails when no Requirements exist in database.
    @attr(all=True, integration=True)
    def test01_add_requirement(self):
        """
        (TestRequirement) add_requirement returns 0 on success and new Requirement data model added to dictionary
        """

        self.assertEqual(self.DUT.request_requirements(0)[1], 0)
        (_results,
         _error_code,
         _requirement_id) = self.DUT.add_requirement(0, 0)

        self.assertTrue(isinstance(self.DUT.dicRequirements[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test02_add_requirement_no_parent(self):
        """
        (TestRequirement) add_requirement uses default parent ID when none is passed
        """

        self.assertEqual(self.DUT.request_requirements(0)[1], 0)
        (_results,
         _error_code,
         _requirement_id) = self.DUT.add_requirement(0)
        self.assertEqual(self.DUT.dicRequirements[self.DUT._last_id].parent_id,
                         -1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test03_delete_requirement(self):
        """
        (TestRequirement) delete_requirement returns 0 on success
        """

        self.assertEqual(self.DUT.request_requirements(0)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_requirement(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, [0, 0])

    @attr(all=True, integration=True)
    def test04_save_requirement(self):
        """
        (TestRequirement) save_requirement returns (True, 0) on success
        """

        self.DUT.request_requirements(0)
        self.assertEqual(self.DUT.save_requirement(1), (True, 0))

    @attr(all=True, integration=True)
    def test05_save_all_requirements(self):
        """
        (TestRequirement) save_all_requirements returns False on success
        """

        self.DUT.request_requirements(0)
        self.assertEqual(self.DUT.save_all_requirements(),
                         [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)])

    @attr(all=True, integration=True)
    def test06_copy_requirements(self):
        """
        (TestRequirement) save_all_requirements returns False on success
        """

        self.DUT.request_requirements(0)
        self.assertFalse(self.DUT.copy_requirements(0))
