#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.tests.unit._dao.TestRTKSiteInfo.py is part of the RTK Project
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
This is the test class for testing the RTKSiteInfo module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSiteInfo import RTKSiteInfo

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSiteInfo(unittest.TestCase):
    """
    Class for testing the RTKSiteInfo class.
    """

    _attributes =(1, '9490059723f3a743fb961d092d3283422f4f2d13',
                  date.today() + timedelta(30))

    def setUp(self):
        """
        Sets up the test fixture for the RTKSiteInfo class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSiteInfo).first()

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkprograminfo_create(self):
        """
        (TestRTKSiteInfo) DUT should create an RTKSiteInfo model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSiteInfo))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_site_info')
        self.assertEqual(self.DUT.site_id, 1)
        self.assertEqual(self.DUT.product_key,
                         '9490059723f3a743fb961d092d3283422f4f2d13')
        self.assertEqual(self.DUT.expire_on, date.today() + timedelta(30))

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSiteInfo) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSiteInfo) set_attributes should return a zero error code on success
        """

        _attributes = ('9490059723f3a743fb961d092d3283422f4f2d13',
                       date.today() + timedelta(365))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSiteInfo {0:d} " \
                               "attributes.".format(self.DUT.site_id))

    @attr(all=True, unit=False)
    def test05b_set_attributes_wrong_type(self):
        """
        (TestRTKSiteInfo) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('9490059723f3a743fb961d092d3283422f4f2d13', -1)


        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKSiteInfo " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test05c_set_attributes_too_few_passed(self):
        """
        (TestRTKSiteInfo) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('9490059723f3a743fb961d092d3283422f4f2d13', )


        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSiteInfo.set_attributes().")
