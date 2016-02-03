#!/usr/bin/env python -O
"""
This is the test class for testing Revision module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       TestRevision.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from revision.Revision import Model, Revision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestRevisionModel(unittest.TestCase):
    """
    Class for testing the Revision model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

        self.good_values = (0, 1, 50.0, 'days', 'Test Mission')
        self.bad_values = (0, 'days', 'Test Mission', 1, 50.0)

        self._reliability_inputs = (0.005, 0.0000065, 0.0000065, 0.0045)
        self._availability_inputs = (1.25, 2.86, 3.18, 2.06)
        self._cost_inputs = 100.00
        self._mission_time = 10.0
        self._hr_multiplier = [1.0, 1000000]

    @attr(all=True, unit=True)
    def test_revision_create(self):
        """
        (TestRevision) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.n_parts, 0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_per_failure, 0.0)
        self.assertEqual(self.DUT.cost_per_hour, 0.0)
        self.assertEqual(self.DUT.active_hazard_rate, 0.0)
        self.assertEqual(self.DUT.dormant_hazard_rate, 0.0)
        self.assertEqual(self.DUT.software_hazard_rate, 0.0)
        self.assertEqual(self.DUT.hazard_rate, 0.0)
        self.assertEqual(self.DUT.mission_hazard_rate, 0.0)
        self.assertEqual(self.DUT.mtbf, 0.0)
        self.assertEqual(self.DUT.mission_mtbf, 0.0)
        self.assertEqual(self.DUT.reliability, 0.0)
        self.assertEqual(self.DUT.mission_reliability, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.availability, 0.0)
        self.assertEqual(self.DUT.mission_availability, 0.0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.code, '')
        self.assertEqual(self.DUT.program_time, 0.0)
        self.assertEqual(self.DUT.program_time_se, 0.0)
        self.assertEqual(self.DUT.program_cost, 0.0)
        self.assertEqual(self.DUT.program_cost_se, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestRequirement) set_attributes should return a 0 error code on success
        """

        _values = (0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 'Revision', 1.0, 1.0, 'Remarks',
                   0, 'Rev Dash', 150.0, 5.2, 156832.49, 56.2)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_requirement_set_attributes_wrong_type(self):
        """
        (TestRequirement) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 'Revision', 1.0, 1.0, 'Remarks',
                   0, 'Rev Dash', 150.0, 5.2, 156832.49, 56.2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_requirement_set_attributes_missing_index(self):
        """
        (TestRequirement) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 'Revision', 1.0, 1.0, 'Remarks',
                   0, 'Rev Dash', 150.0, 5.2, 156832.49)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_requirement_get_attributes(self):
        """
        (TestRequirement) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0.0, 0.0, '', 0,
                          '', 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestRequirement) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 'Revision', 1.0, 1.0, 'Remarks',
                   0, 'Rev Dash', 150.0, 5.2, 156832.49, 56.2)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_calculate_reliability(self):
        """
        (TestRevision) calculate_reliability should return False on success
        """

        self.assertFalse(self.DUT.calculate_reliability(
                            self._reliability_inputs,
                            self._mission_time,
                            self._hr_multiplier[0]))
        self.assertAlmostEqual(self.DUT.hazard_rate, 0.005013)
        self.assertAlmostEqual(self.DUT.mtbf, 199.4813485)
        self.assertAlmostEqual(self.DUT.mission_mtbf, 222.2222222)
        self.assertAlmostEqual(self.DUT.reliability, 0.9511058)
        self.assertAlmostEqual(self.DUT.mission_reliability, 0.9559975)

    @attr(all=True, unit=True)
    def test_calculate_reliability_bad_inputs(self):
        """
        (TestRevision) calculate_reliability should set hazard rates and MTBF to 0.0 with a bad inputs
        """

        self.assertFalse(self.DUT.calculate_reliability(
                            (None, None, None, None),
                            self._mission_time,
                            self._hr_multiplier[0]))
        self.assertAlmostEqual(self.DUT.hazard_rate, 0.0)
        self.assertAlmostEqual(self.DUT.mtbf, 0.0)
        self.assertAlmostEqual(self.DUT.reliability, 1.0)

    @attr(all=True, unit=True)
    def test_calculate_availability(self):
        """
        (TestRevision) calculate_availability should return False on success
        """

        self.DUT.mtbf = 199.4813485
        self.DUT.mission_mtbf = 222.2222222

        self.assertFalse(self.DUT.calculate_availability(
                            self._availability_inputs))
        self.assertAlmostEqual(self.DUT.availability, 0.9984261)
        self.assertAlmostEqual(self.DUT.mission_availability, 0.9985869)

    @attr(all=True, unit=True)
    def test_calculate_availability_bad_inputs(self):
        """
        (TestRevision) calculate_availability should set MTXX to 0.0 with bad inputs
        """

        self.DUT.mtbf = 0.0
        self.DUT.mission_mtbf = 0.0

        self.assertFalse(self.DUT.calculate_availability(
                            (None, None, None, None)))
        self.assertAlmostEqual(self.DUT.availability, 1.0)
        self.assertAlmostEqual(self.DUT.mission_availability, 1.0)

    @attr(all=True, unit=True)
    def test_calculate_costs(self):
        """
        (TestRevision) calculate_costs should return False on success
        """

        self.DUT.hazard_rate = 0.005013

        self.assertFalse(self.DUT.calculate_costs(self._cost_inputs,
                                                  self._mission_time))
        self.assertEqual(self.DUT.cost, 100.0)
        self.assertAlmostEqual(self.DUT.cost_per_failure, 0.5013)
        self.assertAlmostEqual(self.DUT.cost_per_hour, 10.0)


class TestRevisionController(unittest.TestCase):
    """
    Class for testing the Revision data controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Revision()

    @attr(all=True, integration=True)
    def test_request_revisions(self):
        """
        (TestRevision)
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)

    @attr(all=True, integration=True)
    def test_request_revisions(self):
        """
        (TestRevision) request_revisions should return 0 on success
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
# TODO: Test that method fails when no Revisions exist in database.
    @attr(all=True, integration=True)
    def test_add_revision(self):
        """
        (TestRevision) add_revision returns 0 on success and new Requirement data model added to dictionary
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(code='-', name='Original',
                            remarks='This is the baseline revision')

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test_add_revision_no_code(self):
        """
        (TestRevision) add_revision returns 0 on success and new Requirement data model added to dictionary
        """
# TODO: Requires configuration file values to set the default code.
        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(None, name='Original',
                            remarks='This is the baseline revision')

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_revision_no_name(self):
        """
        (TestRevision) add_revision returns 0 with no name passed
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
        (_results,
         _error_code,
         _revision_id) = self.DUT.add_revision(code='-', name=None,
                            remarks='This is the baseline revision')

        self.assertTrue(isinstance(self.DUT.dicRevisions[_revision_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.dicRevisions[_revision_id].name,
                         'New Revision')

    @attr(all=True, integration=True)
    def test_delete_revision(self):
        """
        (TestRevision) delete_revision returns 0 on success
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_revision(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_calculate_revision(self):
        """
        (TestRevision) calculate_revision returns 0 on success
        """

        self.DUT.request_revisions(self._dao)
        self.assertEqual(self.DUT.calculate_revision(0, 10.0, 1.0), 0)

    @attr(all=True, integration=True)
    def test_save_revision(self):
        """
        (TestRevision) save_revision returns (True, 0) on success
        """

        self.DUT.request_revisions(self._dao)
        self.assertEqual(self.DUT.save_revision(1), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_revisions(self):
        """
        (TestRevision) save_all_revisions returns False on success
        """

        self.DUT.request_revisions(self._dao)
        self.assertFalse(self.DUT.save_all_revisions())
