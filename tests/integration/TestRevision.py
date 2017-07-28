#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.integration.TestRevision.py is part of The RTK Project
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
This is the test class for testing Revision module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from revision.Revision import Model, Revision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestRevisionController(unittest.TestCase):
    """
    Class for testing the Revision data controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Revision()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test01_request_revisions(self):
        """
        (TestRevision) request_revisions should return 0 on success
        """

        self.assertEqual(self.DUT.request_revisions()[1], 0)

    @attr(all=True, integration=True)
    def test02_add_revision(self):
        """
        (TestRevision) add_revision returns 0 on success and new Requirement data model added to dictionary
        """

        self.assertEqual(self.DUT.request_revisions()[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(code='-', name='Original',
                                               remarks="This is the baseline \
                                                        revision")

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test02a_add_revision_no_code(self):
        """
        (TestRevision) add_revision returns 0 on success and new Requirement data model added to dictionary
        """
        # TODO: Requires configuration file values to set the default code.
        self.assertEqual(self.DUT.request_revisions()[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(None, name='Original',
                                               remarks="This is the baseline \
                                                        revision")

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test02b_add_revision_no_name(self):
        """
        (TestRevision) add_revision returns 0 with no name passed
        """

        self.assertEqual(self.DUT.request_revisions()[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(code='-', name=None,
                                               remarks="This is the baseline \
                                                        revision")

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.dicRevisions[_revision_id].name,
                         'New Revision')

    @attr(all=True, integration=True)
    def test03_delete_revision(self):
        """
        (TestRevision) delete_revision returns 0 on success
        """

        self.assertEqual(self.DUT.request_revisions()[1], 0)
        (_results,
         _error_code) = self.DUT.delete_revision(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test04_calculate_revision(self):
        """
        (TestRevision) calculate_revision returns 0 on success
        """

        self.DUT.request_revisions()
        self.assertEqual(self.DUT.calculate_revision(0, 10.0, 1.0), 0)

    @attr(all=True, integration=True)
    def test05_save_revision(self):
        """
        (TestRevision) save_revision returns (True, 0) on success
        """

        self.DUT.request_revisions()
        self.assertEqual(self.DUT.save_revision(1), (True, 0))

    @attr(all=True, integration=True)
    def test06_save_all_revisions(self):
        """
        (TestRevision) save_all_revisions returns False on success
        """

        self.DUT.request_revisions()
        self.assertFalse(self.DUT.save_all_revisions())
