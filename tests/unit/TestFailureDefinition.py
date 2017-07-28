#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.failure_definition.TestFailureDefinition.py is part of The RTK
#       Project
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
This is the test class for testing Failure Definition module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from failure_definition.FailureDefinition import Model, FailureDefinition
from dao.DAO import DAO, RTKRevision, RTKFailureDefinition

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFailureDefinitionModel(unittest.TestCase):
    """
    Class for testing the Failure Definition model class.
    """

    def setUp(self):
        """
        (TestFailureDefinition): Method to setup the test fixture for the Failure Definition class.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        _revision = RTKRevision()
        self.dao.db_add(_revision)

        _definition = RTKFailureDefinition()
        _definition.revision_id = _revision.revision_id
        _definition.definition = 'Test Failure Definition 1'
        self.dao.db_add(_definition)

        _definition = RTKFailureDefinition()
        _definition.revision_id = _revision.revision_id
        _definition.definition = 'Test Failure Definition 2'
        self.dao.db_add(_definition)

        self.DUT = Model()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test01_definition_create(self):
        """
        (TestFailureDefinition): __init__ should return instance of a FailureDefition data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.last_id, None)
        self.assertEqual(self.DUT.dao, None)

    @attr(all=True, unit=True)
    def test02a_retrieve_all_definitions(self):
        """
        (TestFailureDefinition): retrieve_all should return an instance of RTKFailureDefinition on success
        """

        _dic_definitions = self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(isinstance(_dic_definitions, dict))
        self.assertTrue(isinstance(_dic_definitions[1], RTKFailureDefinition))

    @attr(all=True, unit=True)
    def test02a_retrieve_single_definition(self):
        """
        (TestFailureDefinition): retrieve should return an instance of the RTKFailureDefinition data model on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _definition = self.DUT.retrieve(1)

        self.assertTrue(isinstance(_definition, RTKFailureDefinition))
        self.assertEqual(_definition.revision_id, 1)
        self.assertEqual(_definition.definition_id, 1)

    @attr(all=True, unit=True)
    def test02b_retrieve_missing_definition(self):
        """
        (TestFailureDefinition): retrieve should return None when passes a Definition ID that doesn't exist.
        """

        _definition = self.DUT.retrieve(100)

        self.assertEqual(_definition, None)

    @attr(all=True, unit=True)
    def test03a_add_definition(self):
        """
        (TestFailureDefinition): add_definition should return an RTKFailureDefinition object on success.
        """

        self.DUT.retrieve_all(self.dao, 1)
        _definition = self.DUT.add_definition(1)

        self.assertTrue(isinstance(_definition, RTKFailureDefinition))
        self.assertEqual(_definition.revision_id, 1)

    @attr(all=True, unit=True)
    def test04a_delete_definition(self):
        """
        (TestFailureDefinition): delete_definition should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertFalse(self.DUT.delete_definition(2))

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_definition_id(self):
        """
        (TestFailureDefinition): delete_definition should return True when passed a Definition ID that doesn't exist.
        """

        self.assertTrue(self.DUT.delete_definition(100))

    @attr(all=True, unit=True)
    def test_05a_save_definition(self):
        """
        (TestFailureDefinition): save_definition should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _definition = self.DUT.dicDefinition[1]
        _definition.definition = 'Definition to save'

        self.assertFalse(self.DUT.save_definition(1))

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_definition(self):
        """
        (TestFailureDefinition): save_definition should return True when passed a Definition ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.save_definition(100))

    @attr(all=True, unit=True)
    def test_06a_save_all_missions(self):
        """
        (TestFailureDefinition): save_all_definitions should return False on success.
        """

        self.assertFalse(self.DUT.save_all_definitions())


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')
        self.dao.db_add(RTKFailureDefinition())
        self.dao.db_add(RTKFailureDefinition())

        self.DUT = FailureDefinition()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test01_create_controller(self):
        """
        (TestFailureDefinition): Test the creation of a Failure Definition data controller instance.
        """

        self.assertTrue(isinstance(self.DUT, FailureDefinition))
        self.assertTrue(isinstance(self.DUT.failure_model, Model))

    @attr(all=True, unit=True)
    def test02a_request_failure_definitions(self):
        """
        (TestFailureDefinition): request_failure_definitions should return a dictionary on success
        """

        _dic_definitions = self.DUT.request_failure_definitions(self.dao, 1)

        self.assertTrue(isinstance(_dic_definitions, dict))
        self.assertTrue(isinstance(_dic_definitions[1], RTKFailureDefinition))
