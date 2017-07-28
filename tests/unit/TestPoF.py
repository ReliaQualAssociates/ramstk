#!/usr/bin/env python -O
"""
This is the test class for testing the Physics of Failure (PoF) class.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestPoF.py is part of The RTK Project

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

from analyses.pof.PhysicsOfFailure import Model, PoF, ParentError


__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPoFModel(unittest.TestCase):
    """
    Class for testing the Physics of Failure model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the PoF model class.
        """

        self.DUT = Model(0)

    @attr(all=True, unit=True)
    def test_pof_create(self):

        """
        (TestPoF) __init__ should return instance of PoF data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicMechanisms, {})
        self.assertEqual(self.DUT.assembly_id, 0)

    @attr(all=True, unit=True)
    def test_pof_create_parent_problem(self):

        """
        (TestPoF) __init__ raises ParentError for None input
        """

        self.assertRaises(ParentError, Model, None)


class TestPoFController(unittest.TestCase):
    """
    Class for testing the PoF data controller class.
    """

    def setUp(self):

        self.DUT = PoF()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestPoF) __init__ should return instance of PoF data controller
        """

        self.assertEqual(self.DUT.dicPoF, {})
