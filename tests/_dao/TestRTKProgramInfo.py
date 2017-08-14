#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKProgramInfo.py is part of the RTK Project
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
This is the test class for testing the RTKProgramInfo module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKProgramInfo import RTKProgramInfo

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKProgramInfo(unittest.TestCase):
    """
    Class for testing the RTKProgramInfo class.
    """

    _attributes =(1, 'REV', 0, 'FUNCTION', 0, 'ASSEMBLY', 0, 'PART', 0,
                  'FMECA', 0, 'MODE', 0, 'EFFECT', 0, 'CAUSE', 0, 'MODULE', 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, date.today(), '',
                  date.today(), '', 'STANDARD')

    def setUp(self):
        """
        Sets up the test fixture for the RTKProgramInfo class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKProgramInfo).first()

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkprograminfo_create(self):
        """
        (TestRTKProgramInfo) DUT should create an RTKProgramInfo model.
        """

        self.assertTrue(isinstance(self.DUT, RTKProgramInfo))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_program_info')
        self.assertEqual(self.DUT.program_id, 1)
        self.assertEqual(self.DUT.revision_prefix, 'REV')
        self.assertEqual(self.DUT.revision_next_id, 0)
        self.assertEqual(self.DUT.function_prefix, 'FUNCTION')
        self.assertEqual(self.DUT.function_next_id, 0)
        self.assertEqual(self.DUT.assembly_prefix, 'ASSEMBLY')
        self.assertEqual(self.DUT.assembly_next_id, 0)
        self.assertEqual(self.DUT.part_prefix, 'PART')
        self.assertEqual(self.DUT.part_next_id, 0)
        self.assertEqual(self.DUT.fmeca_prefix, 'FMECA')
        self.assertEqual(self.DUT.fmeca_next_id, 0)
        self.assertEqual(self.DUT.mode_prefix, 'MODE')
        self.assertEqual(self.DUT.mode_next_id, 0)
        self.assertEqual(self.DUT.effect_prefix, 'EFFECT')
        self.assertEqual(self.DUT.effect_next_id, 0)
        self.assertEqual(self.DUT.cause_prefix, 'CAUSE')
        self.assertEqual(self.DUT.cause_next_id, 0)
        self.assertEqual(self.DUT.software_prefix, 'MODULE')
        self.assertEqual(self.DUT.software_next_id, 0)
        self.assertEqual(self.DUT.revision_active, 1)
        self.assertEqual(self.DUT.function_active, 1)
        self.assertEqual(self.DUT.requirement_active, 1)
        self.assertEqual(self.DUT.hardware_active, 1)
        self.assertEqual(self.DUT.software_active, 1)
        self.assertEqual(self.DUT.vandv_active, 1)
        self.assertEqual(self.DUT.testing_active, 1)
        self.assertEqual(self.DUT.fraca_active, 1)
        self.assertEqual(self.DUT.survival_active, 1)
        self.assertEqual(self.DUT.rcm_active, 0)
        self.assertEqual(self.DUT.rbd_active, 0)
        self.assertEqual(self.DUT.fta_active, 0)
        self.assertEqual(self.DUT.created_on, date.today())
        self.assertEqual(self.DUT.created_by, '')
        self.assertEqual(self.DUT.last_saved, date.today())
        self.assertEqual(self.DUT.last_saved_by, '')
        self.assertEqual(self.DUT.method, 'STANDARD')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKProgramInfo) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKProgramInfo) set_attributes should return a zero error code on success
        """

        _attributes = ('REVISION', 0, 'FUNCTION', 0, 'ASSEMBLY', 0, 'PART', 0,
                       'FMECA', 0, 'MODE', 0, 'EFFECT', 0, 'CAUSE', 0,
                       'MODULE', 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       date.today(), '', date.today(), '', 'STANDARD')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKProgramInfo {0:d} " \
                               "attributes.".format(self.DUT.program_id))

    @attr(all=True, unit=True)
    def test05b_set_attributes_wrong_type(self):
        """
        (TestRTKProgramInfo) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('REVISION', 0, 'FUNCTION', 0, 'ASSEMBLY', 0, 'PART', 0,
                       'FMECA', 0, 'MODE', 0, 'EFFECT', 0, 'CAUSE', 0,
                       'MODULE', 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, None,
                       date.today(), '', date.today(), '', 'STANDARD')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKProgramInfo " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test05c_set_attributes_too_few_passed(self):
        """
        (TestRTKProgramInfo) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('REVISION', 0, 'FUNCTION', 0, 'ASSEMBLY', 0, 'PART', 0,
                       'FMECA', 0, 'MODE', 0, 'EFFECT', 0, 'CAUSE', 0,
                       'MODULE', 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       date.today(), '', date.today())

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKProgramInfo.set_attributes().")
