#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestHardwareBoM.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from datetime import date
import pandas as pd

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import Utilities as Utilities  # pylint: disable=E0401, wrong-import-position
# pylint: disable=E0401, wrong-import-position
from Configuration import Configuration
# pylint: disable=E0401, wrong-import-position
from hardware import dtmHardware, dtmDesignElectric, dtmDesignMechanic, \
    dtmMilHdbkF, dtmNSWC, dtmReliability, dtmHardwareBoM, dtcHardwareBoM
from dao import DAO  # pylint: disable=E0401, wrong-import-position
# pylint: disable=E0401, wrong-import-position
from dao import RTKHardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestHardwareBoMDataModel(unittest.TestCase):
    """Class for testing the Hardware BoM data model class."""

    def setUp(self):
        """(TestHardwareBoMDataModel) Set up the test fixture for the Hardware BoM class."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmHardwareBoM(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestHardwareBoMDataModel) __init__ should return a Hardware BoM model."""
        self.assertTrue(isinstance(self.DUT, dtmHardwareBoM))
        self.assertTrue(isinstance(self.DUT.dtm_hardware, dtmHardware))
        self.assertTrue(
            isinstance(self.DUT.dtm_design_electric, dtmDesignElectric))
        self.assertTrue(
            isinstance(self.DUT.dtm_design_mechanic, dtmDesignMechanic))
        self.assertTrue(isinstance(self.DUT.dtm_mil_hdbk_f, dtmMilHdbkF))
        self.assertTrue(isinstance(self.DUT.dtm_nswc, dtmNSWC))
        self.assertTrue(isinstance(self.DUT.dtm_reliability, dtmReliability))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        # pylint: disable=protected-access
        self.assertEqual(self.DUT._tag, 'HardwareBoM')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestHardwareBoMDataModel) select_all() should return a Tree() object populated with RTKHardware instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, dict))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestHardwareBoMDataModel) select() should return an instance of the RTKHardware data model on success."""
        self.DUT.select_all(1)
        _hardware = self.DUT.select(1, 'general')

        self.assertTrue(isinstance(_hardware, RTKHardware))
        self.assertEqual(_hardware.ref_des, 'S1')
        self.assertEqual(_hardware.cage_code, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestHardwareBoMDataModel) select() should return None when a non-existent Hardware ID is requested."""
        _hardware = self.DUT.select(100, 'general')

        self.assertEqual(_hardware, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling_assembly(self):
        """(TestHardwareBoMDataModel) insert() should return a zero error code on success when inserting a sibling Hardware assembly."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0, part=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test03b_insert_child_assembly(self):
        """(TestHardwareBoMDataModel) insert() should return a zero error code on success when inserting a child Hardware assembly."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1, part=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

    @attr(all=True, unit=True)
    def test03c_insert_part(self):
        """(TestHardwareBoMDataModel) insert() should return a zero error code on success when inserting a child Hardware piece part."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1, part=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 5)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestHardwareBoMDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')
        self.assertEqual(self.DUT.last_id, 3)

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestHardwareBoMDataModel) delete() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                         'Hardware BoM record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestHardwareBoMDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _hardware = self.DUT.tree.get_node(1).data
        _hardware['cost'] = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestHardwareBoMDataModel) update() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 12036)
        self.assertEqual(
            _msg,
            'RTK ERROR: Attempted to save non-existent Hardware ID 100.\n'
            'RTK ERROR: Attempted to save non-existent Reliability record ID 100.\n'
            'RTK ERROR: Attempted to save non-existent DesignElectric record ID 100.\n'
            'RTK ERROR: Attempted to save non-existent DesignMechanic record ID 100.\n'
            'RTK ERROR: Attempted to save non-existent MilHdbkF record ID 100.\n'
            'RTK ERROR: Attempted to save non-existent NSWC record ID 100.\n')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestHardwareBoMDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class TestHardwareBoMDataController(unittest.TestCase):
    """Class for testing the Usage Profile controller class."""

    _attributes = {
        'revision_id': 1,
        'hardware_id': 1,
        'alt_part_num': '',
        'attachments': '',
        'cage_code': '',
        'category_id': 0,
        'comp_ref_des': 'S1',
        'cost': 0.0,
        'cost_failure': 0.0,
        'cost_hour': 0.0,
        'cost_type_id': 0,
        'description': 'Description',
        'duty_cycle': 100.0,
        'figure_number': '',
        'lcn': '',
        'level': 0,
        'manufacturer_id': 0,
        'mission_time': 100.0,
        'name': '',
        'nsn': '',
        'page_number': '',
        'parent_id': 0,
        'part': 0,
        'part_number': '',
        'quantity': 1,
        'ref_des': '',
        'remarks': '',
        'repairable': 0,
        'specification_number': '',
        'subcategory_id': 0,
        'tagged_part': 0,
        'total_part_count': 0,
        'total_power_dissipation': 0,
        'year_of_manufacture': date.today().year,
        'voltage_ac_operating': 0.0,
        'frequency_operating': 0.0,
        'type_id': 0,
        'resistance': 0.0,
        'package_id': 0,
        'technology_id': 0,
        'n_cycles': 0,
        'n_circuit_planes': 1,
        'contact_gauge': 0,
        'current_operating': 0.0,
        'n_hand_soldered': 0,
        'contact_rating_id': 0,
        'area': 0.0,
        'contact_form_id': 0,
        'years_in_production': 1,
        'n_active_pins': 0,
        'capacitance': 0.0,
        'temperature_case': 0.0,
        'current_rated': 0.0,
        'power_operating': 0.0,
        'configuration_id': 0,
        'temperature_hot_spot': 0.0,
        'temperature_junction': 0.0,
        'current_ratio': 0.0,
        'insulation_id': 0,
        'construction_id': 0,
        'insert_id': 0,
        'theta_jc': 0.0,
        'voltage_dc_operating': 0.0,
        'power_ratio': 0.0,
        'family_id': 0,
        'overstress': 1,
        'voltage_rated': 0.0,
        'feature_size': 0.0,
        'operating_life': 0.0,
        'application_id': 0,
        'weight': 0.0,
        'temperature_rated_max': 0.0,
        'voltage_ratio': 0.0,
        'temperature_rated_min': 0.0,
        'power_rated': 0.0,
        'environment_active_id': 0,
        'specification_id': 0,
        'matching_id': 0,
        'n_elements': 0,
        'environment_dormant_id': 0,
        'reason': u'',
        'voltage_esd': 0.0,
        'manufacturing_id': 0,
        'n_wave_soldered': 0,
        'temperature_rise': 0.0,
        'temperature_active': 35.0,
        'temperature_dormant': 25.0,
        'pressure_upstream': 0.0,
        'surface_finish': 0.0,
        'friction': 0.0,
        'length_compressed': 0.0,
        'load_id': 0,
        'balance_id': 0,
        'lubrication_id': 0,
        'water_per_cent': 0.0,
        'misalignment_angle': 0.0,
        'rpm_design': 0.0,
        'pressure_downstream': 0.0,
        'diameter_coil': 0.0,
        'pressure_contact': 0.0,
        'meyer_hardness': 0.0,
        'rpm_operating': 0.0,
        'length_relaxed': 0.0,
        'impact_id': 0,
        'n_ten': 0,
        'material_id': 0,
        'service_id': 0,
        'flow_design': 0.0,
        'diameter_wire': 0.0,
        'deflection': 0.04,
        'filter_size': 0.0,
        'diameter_inner': 0.0,
        'pressure_rated': 0.0,
        'altitude_operating': 0.0,
        'thickness': 0.0,
        'diameter_outer': 0.0,
        'contact_pressure': 0.0,
        'particle_size': 0.0,
        'casing_id': 0,
        'viscosity_dynamic': 0.0,
        'viscosity_design': 0.0,
        'torque_id': 0,
        'leakage_allowable': 0.0,
        'offset': 0.0,
        'width_minimum': 0.0,
        'load_operating': 0.0,
        'spring_index': 0.0,
        'flow_operating': 0.0,
        'pressure_delta': 0.0,
        'length': 0.0,
        'load_design': 0.0,
        'clearance': 0.0,
        'piP': 0.0,
        'piC': 0.0,
        'piPT': 0.0,
        'piR': 0.0,
        'piA': 0.0,
        'piK': 0.0,
        'lambdaEOS': 0.00056,
        'piNR': 0.0,
        'piCF': 0.0,
        'piMFG': 0.0,
        'piM': 0.0,
        'piI': 0.0,
        'lambdaBP': 0.0,
        'piL': 0.0,
        'piCYC': 0.0,
        'piN': 0.0,
        'piF': 0.0,
        'lambdaCYC': 0.0,
        'piCV': 0.0,
        'piE': 0.0,
        'piCR': 0.0,
        'A1': 0.00235,
        'piQ': 0.0,
        'A2': 0.0,
        'B1': 0.0,
        'B2': 0.0,
        'lambdaBD': 0.0,
        'piCD': 0.0,
        'C2': 0.0,
        'C1': 0.0,
        'piS': 0.0,
        'piT': 0.0,
        'piU': 0.0,
        'piV': 0.0,
        'piTAPS': 0.0,
        'Clc': 0.0,
        'Crd': 0.0,
        'Cac': 0.0,
        'Cmu': 0.0,
        'Ck': 0.0,
        'Ci': 0.0,
        'Ch': 0.0,
        'Cn': 0.0,
        'Cm': 0.0,
        'Cl': 0.0,
        'Cc': 0.0,
        'Cb': 0.0,
        'Cg': 0.0,
        'Cf': 0.0,
        'Ce': 0.0,
        'Cd': 0.0,
        'Cy': 0.0,
        'Cbv': 0.0,
        'Cbt': 0.0,
        'Cs': 0.0,
        'Cr': 0.0,
        'Cq': 0.0,
        'Cp': 0.0,
        'Cw': 0.0,
        'Cv': 0.0,
        'Ct': 0.0,
        'Cnw': 0.0,
        'Cnp': 0.0,
        'Csf': 0.0,
        'Calt': 0.0,
        'Csc': 0.0,
        'Cbl': 0.0,
        'Csz': 0.0,
        'Cst': 0.0,
        'Csw': 0.0,
        'Csv': 0.0,
        'Cgl': 0.0,
        'Cga': 0.0,
        'Cgp': 0.0,
        'Cgs': 0.0,
        'Cgt': 0.0,
        'Cgv': 0.0,
        'Ccw': 0.0,
        'Ccv': 0.0,
        'Cpd': 0.0,
        'Ccp': 0.0,
        'Cpf': 0.0,
        'Ccs': 0.0,
        'Ccf': 0.0,
        'Cpv': 0.0,
        'Cdc': 0.0,
        'Cdl': 0.0,
        'Cdt': 0.0,
        'Cdw': 0.0,
        'Cdp': 0.0,
        'Cds': 0.0,
        'Cdy': 0.0,
        'hazard_rate_percent': 0.0,
        'reliability_mission': 1.0,
        'reliability_goal_measure_id': 0,
        'hazard_rate_specified': 0.0,
        'hazard_rate_active': 0.05,
        'hr_mission_variance': 0.0,
        'reliability_goal': 0.0,
        'mtbf_log_variance': 0.0,
        'quality_id': 0,
        'scale_parameter': 0.0,
        'add_adj_factor': 0.0,
        'availability_mission': 1.0,
        'mtbf_spec_variance': 0.0,
        'mtbf_miss_variance': 0.0,
        'lambda_b': 0.0,
        'hr_specified_variance': 0.0,
        'avail_log_variance': 0.0,
        'hazard_rate_type_id': 0,
        'mtbf_mission': 0.0,
        'failure_distribution_id': 0,
        'reliability_miss_variance': 0.0,
        'avail_mis_variance': 0.0,
        'hazard_rate_method_id': 0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_software': 0.0,
        'mtbf_specified': 0.0,
        'hr_logistics_variance': 0.0,
        'shape_parameter': 0.0,
        'hr_dormant_variance': 0.0,
        'location_parameter': 0.0,
        'survival_analysis_id': 0,
        'hazard_rate_logistics': 0.0,
        'reliability_logistics': 1.0,
        'hazard_rate_model': 'Test HR Model',
        'reliability_log_variance': 0.0,
        'hr_active_variance': 0.0,
        'availability_logistics': 1.0,
        'hazard_rate_dormant': 0.0,
        'mtbf_logistics': 0.0,
        'mult_adj_factor': 1.0,
        'temperature_knee': 25.0,
        'total_cost': 0.0
    }

    def setUp(self):
        """Set up the test fixture for the Mission Data Controller."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcHardwareBoM(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestHardwareBoMDataController) __init__() should create an instance of a Hardware data controller."""
        self.assertTrue(isinstance(self.DUT, dtcHardwareBoM))
        # pylint: disable=protected-access
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmHardwareBoM))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """(TestHardwareBoMDataController) request_select_all() should return a treelib Tree() with the Hardware BoM."""
        self.assertTrue(isinstance(self.DUT.request_select_all(1), Tree))

    @attr(all=True, unit=True)
    def test01b_request_select_all_matrix(self):
        """(TestHardwareBoMDataController) select_all_matrix() should return a tuple containing the matrix, column headings, and row headings."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'hrdwr_vldtn')

        self.assertTrue(isinstance(_matrix, pd.DataFrame))
        self.assertEqual(_column_hdrs, {1: 'Test Validation Task'})
        self.assertEqual(_row_hdrs, {1: u'', 2: u'', 3: u''})

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """(TestHardwareBoMDataController) request_select() should return an instance of the RTKHardware data model on success."""
        self.DUT.request_select_all(1)
        _hardware = self.DUT.request_select(1, 'general')

        self.assertTrue(isinstance(_hardware, RTKHardware))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """(TestHardwareBoMDataController) request_select() should return None when requesting a Hardware item that doesn't exist."""
        _hardware = self.DUT.request_select(100, 'general')

        self.assertEqual(_hardware, None)

    @attr(all=True, unit=True)
    def test03a_request_insert_sibling(self):
        """(TestHardwareBoMDataController) request_insert() should return False on success when inserting a sibling Hardware item."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1, 0))

        self.DUT.request_delete(self.DUT.request_last_id())

    @attr(all=True, unit=True)
    def test03a_request_insert_child(self):
        """(TestHardwareBoMDataController) request_insert() should return False on success when inserting a child Hardware item."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1, 1))

    @attr(all=True, unit=True)
    def test03c_insert_matrix_row(self):
        """(TestHardwareBoMDataController) request_insert_matrix() should return False on successfully inserting a row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'hrdwr_vldtn')

        self.assertFalse(
            self.DUT.request_insert_matrix('hrdwr_vldtn', 4, 'S1:SS1:A1'))
        self.assertEqual(self.DUT._dmx_hw_vldtn_matrix.dic_row_hdrs[4],
                         'S1:SS1:A1')

    @attr(all=True, unit=True)
    def test03d_insert_matrix_duplicate_row(self):
        """(TestHardwareBoMDataController) request_insert_matrix() should return True when attempting to insert a duplicate row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'hrdwr_vldtn')

        self.assertTrue(
            self.DUT.request_insert_matrix('hrdwr_vldtn', 2, 'S1:SS1:A2'))

    @attr(all=True, unit=True)
    def test03e_insert_matrix_column(self):
        """(TestHardwareBoMDataController) request_insert_matrix() should return False on successfully inserting a column."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'hrdwr_vldtn')

        self.assertFalse(
            self.DUT.request_insert_matrix(
                'hrdwr_vldtn', 2, 'Test Validation Task 2', row=False))
        self.assertEqual(self.DUT._dmx_hw_vldtn_matrix.dic_column_hdrs[2],
                         'Test Validation Task 2')

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """(TestHardwareBoMDataController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(self.DUT.request_last_id()))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """(TestHardwareBoMDataController) request_delete() should return True when attempting to delete a non-existent Node ID."""
        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(222))

    @attr(all=True, unit=True)
    def test05a_request_get_attributes(self):
        """(TestHardwareBoMDataController) request_get_attributes() should return a dict of {attribute name:attribute value} pairs for the RTKHardware table."""
        self.DUT.request_select_all(1)

        _attributes = self.DUT.request_get_attributes(1)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_attributes['revision_id'], 1)

    @attr(all=True, unit=True)
    def test06a_request_set_attributes(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return False on success when setting the attributes."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_set_attributes(1, self._attributes))

    @attr(all=True, unit=True)
    def test06b_request_set_attributes_missing_design_electric(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return True when an attribute for the RTKDesignElectric table is missing."""
        self.DUT.request_select_all(1)
        self._attributes.pop('voltage_ac_operating')

        self.assertTrue(self.DUT.request_set_attributes(1, self._attributes))

        self._attributes['voltage_ac_operating'] = 0.0

    @attr(all=True, unit=True)
    def test06c_request_set_attributes_missin_design_mechanic(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return True when an attribute for the RTKDesignMechanic table is missing."""
        self.DUT.request_select_all(1)
        self._attributes.pop('pressure_upstream')

        self.assertTrue(self.DUT.request_set_attributes(1, self._attributes))

        self._attributes['pressure_upstream'] = 0.0

    @attr(all=True, unit=True)
    def test06d_request_set_attributes_missing_mil_hdbk_f(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return True when an attribute for the RTKMilHdbkF table is missing."""
        self.DUT.request_select_all(1)
        self._attributes.pop('piP')

        self.assertTrue(self.DUT.request_set_attributes(1, self._attributes))

        self._attributes['piP'] = 0.0

    @attr(all=True, unit=True)
    def test06e_request_set_attributes_missing_nswc(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return True when an attribute for the RTKNSWC table is missing."""
        self.DUT.request_select_all(1)
        self._attributes.pop('Clc')

        self.assertTrue(self.DUT.request_set_attributes(1, self._attributes))

        self._attributes['Clc'] = 0.0

    @attr(all=True, unit=True)
    def test06f_request_set_attributes_missing_reliability(self):
        """(TestHardwareBoMDataController) request_set_attributes() should return True when an attribute for the RTKReliability table is missing."""
        self.DUT.request_select_all(1)
        self._attributes.pop('hazard_rate_percent')

        self.assertTrue(self.DUT.request_set_attributes(1, self._attributes))

        self._attributes['hazard_rate_percent'] = 0.0

    @attr(all=True, unit=True)
    def test07a_request_last_id(self):
        """(TestHardwareBoMDataController) request_last_id() should return the last Hardware ID used in the RTK Program database."""
        self.DUT.request_select_all(1)

        self.assertEqual(self.DUT.request_last_id(), 3)

    @attr(all=True, unit=True)
    def test08a_request_update_all(self):
        """(TestHardwareBoMDataController) request_update_all() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test09a_request_make_composite_reference_designator(self):
        """(TestHardwareBoMDataController) request_make_composite_reference_designator() should return a zero error code on success."""
        self.DUT.request_select_all(1)

        (_error_code, _msg
         ) = self.DUT.request_make_composite_reference_designator(node_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, '')
        self.assertEqual(
            self.DUT.request_get_attributes(2)['comp_ref_des'], 'S1:SS1')
