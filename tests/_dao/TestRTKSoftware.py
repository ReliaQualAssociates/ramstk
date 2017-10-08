#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSoftware.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSoftware module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSoftware import RTKSoftware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSoftware(unittest.TestCase):
    """
    Class for testing the RTKSoftware class.
    """

    _attributes =(1, 1, 0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0,
                  'Test Software Description', 0, 0, 0.0, 0.0, 0.0, 0, 0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0,
                  0, 0, 0.0, 0.0, 0.0, 0, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftware class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSoftware).first()
        self.DUT.description = self._attributes[16]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtksoftware_create(self):
        """
        (TestRTKSoftware) __init__ should create an RTKSoftware model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftware))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.a, 0.0)
        self.assertEqual(self.DUT.aloc, 0)
        self.assertEqual(self.DUT.am, 0.0)
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.ax, 0)
        self.assertEqual(self.DUT.budget_test, 0.0)
        self.assertEqual(self.DUT.budget_dev, 0.0)
        self.assertEqual(self.DUT.bx, 0)
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.cb, 0)
        self.assertEqual(self.DUT.cx, 0)
        self.assertEqual(self.DUT.d, 0.0)
        self.assertEqual(self.DUT.dc, 0.0)
        self.assertEqual(self.DUT.dd, 0)
        self.assertEqual(self.DUT.description, 'Test Software Description')
        self.assertEqual(self.DUT.development_id, 0)
        self.assertEqual(self.DUT.dev_assess_type_id, 0)
        self.assertEqual(self.DUT.df, 0.0)
        self.assertEqual(self.DUT.do, 0.0)
        self.assertEqual(self.DUT.dr, 0.0)
        self.assertEqual(self.DUT.dr_eot, 0)
        self.assertEqual(self.DUT.dr_test, 0)
        self.assertEqual(self.DUT.e, 0.0)
        self.assertEqual(self.DUT.ec, 0.0)
        self.assertEqual(self.DUT.et, 0.0)
        self.assertEqual(self.DUT.ev, 0.0)
        self.assertEqual(self.DUT.ew, 0.0)
        self.assertEqual(self.DUT.f, 0.0)
        self.assertEqual(self.DUT.ft1, 0.0)
        self.assertEqual(self.DUT.ft2, 0.0)
        self.assertEqual(self.DUT.hloc, 0)
        self.assertEqual(self.DUT.labor_hours_dev, 0.0)
        self.assertEqual(self.DUT.labor_hours_test, 0.0)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.loc, 0)
        self.assertEqual(self.DUT.n_branches, 0)
        self.assertEqual(self.DUT.n_branches_test, 0)
        self.assertEqual(self.DUT.n_inputs, 0)
        self.assertEqual(self.DUT.n_inputs_test, 0)
        self.assertEqual(self.DUT.n_interfaces, 0)
        self.assertEqual(self.DUT.n_interfaces_test, 0)
        self.assertEqual(self.DUT.ncb, 0)
        self.assertEqual(self.DUT.nm, 0)
        self.assertEqual(self.DUT.nm_test, 0)
        self.assertEqual(self.DUT.os, 0.0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.ren_avg, 0.0)
        self.assertEqual(self.DUT.ren_eot, 0.0)
        self.assertEqual(self.DUT.rpfom, 0.0)
        self.assertEqual(self.DUT.s1, 0.0)
        self.assertEqual(self.DUT.s2, 0.0)
        self.assertEqual(self.DUT.sa, 0.0)
        self.assertEqual(self.DUT.schedule_dev, 0.0)
        self.assertEqual(self.DUT.schedule_test, 0.0)
        self.assertEqual(self.DUT.sl, 0.0)
        self.assertEqual(self.DUT.sm, 0.0)
        self.assertEqual(self.DUT.sq, 0.0)
        self.assertEqual(self.DUT.sr, 0.0)
        self.assertEqual(self.DUT.st, 0.0)
        self.assertEqual(self.DUT.sx, 0.0)
        self.assertEqual(self.DUT.t, 0.0)
        self.assertEqual(self.DUT.tc, 0.0)
        self.assertEqual(self.DUT.tcl, 0)
        self.assertEqual(self.DUT.te, 0.0)
        self.assertEqual(self.DUT.test_approach, 0)
        self.assertEqual(self.DUT.test_effort, 0)
        self.assertEqual(self.DUT.test_path, 0)
        self.assertEqual(self.DUT.test_time, 0.0)
        self.assertEqual(self.DUT.test_time_eot, 0.0)
        self.assertEqual(self.DUT.tm, 0.0)
        self.assertEqual(self.DUT.um, 0)
        self.assertEqual(self.DUT.wm, 0)
        self.assertEqual(self.DUT.xm, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSoftware) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSoftware) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0,
                       'Test Software Description', 0, 0, 0.0, 0.0, 0.0, 0, 0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSoftware {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSoftware) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0,
                       'Test Software Description', 0, 0, 0.0, 0.0, 0.0, 0, 0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 'None', 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKSoftware " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSoftware) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0,
                       'Test Software Description', 0, 0, 0.0, 0.0, 0.0, 0, 0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSoftware.set_attributes().")
