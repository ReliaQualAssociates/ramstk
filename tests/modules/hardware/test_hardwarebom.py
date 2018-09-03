#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_hardwarebom.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models. """

from datetime import date
import pandas as pd
from treelib import Tree

import pytest

from rtk.modules.hardware import (
    dtmHardware, dtmDesignElectric, dtmDesignMechanic, dtmMilHdbkF, dtmNSWC,
    dtmReliability, dtmHardwareBoM, dtcHardwareBoM)
from rtk.dao import DAO, RAMSTKHardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

ATTRIBUTES = {
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


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a Hardware BoM model. """
    DUT = dtmHardwareBoM(test_dao)

    assert isinstance(DUT, dtmHardwareBoM)
    assert isinstance(DUT.dtm_hardware, dtmHardware)
    assert isinstance(DUT.dtm_design_electric, dtmDesignElectric)
    assert isinstance(DUT.dtm_design_mechanic, dtmDesignMechanic)
    assert isinstance(DUT.dtm_mil_hdbk_f, dtmMilHdbkF)
    assert isinstance(DUT.dtm_nswc, dtmNSWC)
    assert isinstance(DUT.dtm_reliability, dtmReliability)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'HardwareBoM'


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKHardware instances on success. """
    DUT = dtmHardwareBoM(test_dao)

    _tree = DUT.do_select_all(revision_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, dict)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKHardware data model on success. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='general')

    assert isinstance(_hardware, RAMSTKHardware)
    assert _hardware.ref_des == 'S1'
    assert _hardware.cage_code == ''


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Hardware ID is requested. """
    DUT = dtmHardwareBoM(test_dao)

    assert DUT.do_select(100, table='general') is None


@pytest.mark.integration
def test_do_insert_sibling_assembly(test_dao):
    """ do_insert() should return a zero error code on success when inserting a sibling Hardware assembly. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=0, part=0)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding a new hardware item to the RAMSTK "
                    "Program database.")


@pytest.mark.integration
def test_do_insert_child_assembly(test_dao):
    """ do_insert() should return a zero error code on success when inserting a child Hardware assembly. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=1, part=0)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding a new hardware item to the RAMSTK "
                    "Program database.")


@pytest.mark.integration
def test_do_insert_part(test_dao):
    """ do_insert() should return a zero error code on success when inserting a child Hardware piece part. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1, parent_id=1, part=1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding a new hardware item to the RAMSTK "
                    "Program database.")


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Hardware ID that doesn't exist. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ('RAMSTK ERROR: Attempted to delete non-existent Hardware BoM '
                    'record ID 300.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='general')
    _hardware.cost = 0.9832

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Hardware ID that doesn't exist. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 12036
    #assert _msg == ('RAMSTK ERROR: Attempted to save non-existent Hardware ID '
    #                '100.\n  RAMSTK ERROR: Attempted to save non-existent '
    #                'Reliability record ID 100.\n  RAMSTK ERROR: Attempted to '
    #                'save non-existent DesignElectric record ID 100.\n  RAMSTK '
    #                'ERROR: Attempted to save non-existent DesignMechanic '
    #                'record ID 100.\n  RAMSTK ERROR: Attempted to save '
    #                'non-existent MilHdbkF record ID 100.\n  RAMSTK ERROR: '
    #                'Attempted to save non-existent NSWC record ID 100.\n')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmHardwareBoM(test_dao)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the hardware bill "
                    "of materials.")


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should create an instance of a Hardware data controller. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcHardwareBoM)
    assert isinstance(DUT._dtm_data_model, dtmHardwareBoM)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a treelib Tree() with the Hardware BoM. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)

    assert isinstance(DUT.request_do_select_all(revision_id=1), Tree)


@pytest.mark.integration
def test_request_do_select_all_matrix(test_dao, test_configuration):
    """ request_do_select_all_matrix() should return a tuple containing the matrix, column headings, and row headings. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)

    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'hrdwr_vldtn')

    assert isinstance(_matrix, pd.DataFrame)
    assert _column_hdrs[1] == ''
    assert _row_hdrs[1] == 'S1'
    assert _row_hdrs[2] == 'S1:SS1'
    assert _row_hdrs[3] == 'S1:SS2'
    assert _row_hdrs[4] == 'S1:SS3'


@pytest.mark.integration
def test_request_do_update_matrix(test_dao, test_configuration):
    """ request_do_update_matrix() should return False on success. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    DUT.request_do_select_all_matrix(1, 'hrdwr_vldtn')

    assert not DUT.request_do_update_matrix(1, 'hrdwr_vldtn')


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an instance of the RAMSTKHardware data model on success. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    _hardware = DUT.request_do_select(1, table='general')

    assert isinstance(_hardware, RAMSTKHardware)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Hardware item that doesn't exist. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)

    _hardware = DUT.request_do_select(100, table='general')

    assert _hardware is None


@pytest.mark.integration
def test_request_do_insert_sibling(test_dao, test_configuration):
    """ request_do_insert() should return False on success when inserting a sibling Hardware item. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    DUT.request_do_select_all_matrix(1, 'hrdwr_rqrmnt')
    DUT.request_do_select_all_matrix(1, 'hrdwr_vldtn')

    assert not DUT.request_do_insert(revision_id=1, parent_id=0, part=0)


@pytest.mark.integration
def test_request_do_insert_child(test_dao, test_configuration):
    """ request_do_insert() should return False on success when inserting a child Hardware item. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    DUT.request_do_select_all_matrix(1, 'hrdwr_rqrmnt')
    DUT.request_do_select_all_matrix(1, 'hrdwr_vldtn')

    assert not DUT.request_do_insert(revision_id=1, parent_id=1, part=0)


@pytest.mark.integration
def test_request_do_insert_matrix_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'hrdwr_vldtn')

    assert not DUT.request_do_insert_matrix('hrdwr_vldtn', 13, 'S1:SS1:A13')
    assert DUT._dmx_hw_vldtn_matrix.dic_row_hdrs[13] == 'S1:SS1:A13'


@pytest.mark.integration
def test_request_do_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ request_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'hrdwr_vldtn')

    assert DUT.request_do_insert_matrix('hrdwr_vldtn', 2, 'S1:SS1:A2')


@pytest.mark.integration
def test_request_do_insert_matrix_column(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)
    (_matrix, _column_hdrs, _row_hdrs) = DUT.request_do_select_all_matrix(
        1, 'hrdwr_vldtn')

    if pytest.mark.name == 'integration':
        assert not DUT.request_insert_matrix(
            'hrdwr_vldtn', 1, 'Test Validation Task 1', row=False)
        assert DUT._dmx_hw_vldtn_matrix.dic_column_hdrs[
            1] == 'Test Validation Task 1'
    elif pytest.mark.name == 'hardware':
        assert not DUT.request_insert_matrix(
            'hrdwr_vldtn', 2, 'Test Validation Task 2', row=False)
        assert DUT._dmx_hw_vldtn_matrix.dic_column_hdrs[
            2] == 'Test Validation Task 2'


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Node ID. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert DUT.request_do_delete(222)


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs for the RAMSTKHardware table. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['revision_id'] == 1


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return False on success when setting the attributes. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_set_attributes(1, ATTRIBUTES)


@pytest.mark.integration
def test_request_set_attributes_missing_design_electric(
        test_dao, test_configuration):
    """ request_set_attributes() should return True when an attribute for the RAMSTKDesignElectric table is missing. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    ATTRIBUTES.pop('voltage_ac_operating')

    assert DUT.request_set_attributes(1, ATTRIBUTES)

    ATTRIBUTES['voltage_ac_operating'] = 0.0


@pytest.mark.integration
def test_request_set_attributes_missing_design_mechanic(
        test_dao, test_configuration):
    """ request_set_attributes() should return True when an attribute for the RAMSTKDesignMechanic table is missing. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    ATTRIBUTES.pop('pressure_upstream')

    assert DUT.request_set_attributes(1, ATTRIBUTES)

    ATTRIBUTES['pressure_upstream'] = 0.0


@pytest.mark.integration
def test_request_set_attributes_missing_mil_hdbk_f(test_dao,
                                                   test_configuration):
    """ request_set_attributes() should return True when an attribute for the RAMSTKMilHdbkF table is missing. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    ATTRIBUTES.pop('piP')

    assert DUT.request_set_attributes(1, ATTRIBUTES)

    ATTRIBUTES['piP'] = 0.0


@pytest.mark.integration
def test_request_set_attributes_missing_nswc(test_dao, test_configuration):
    """ request_set_attributes() should return True when an attribute for the RAMSTKNSWC table is missing. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    ATTRIBUTES.pop('Clc')

    assert DUT.request_set_attributes(1, ATTRIBUTES)

    ATTRIBUTES['Clc'] = 0.0


@pytest.mark.integration
def test_request_set_attributes_missing_reliability(test_dao,
                                                    test_configuration):
    """ request_set_attributes() should return True when an attribute for the RAMSTKReliability table is missing. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    ATTRIBUTES.pop('hazard_rate_percent')

    assert DUT.request_set_attributes(1, ATTRIBUTES)

    ATTRIBUTES['hazard_rate_percent'] = 0.0


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Hardware ID used in the RAMSTK Program database. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    if pytest.mark.name == 'integration':
        assert DUT.request_last_id() == 12
    else:
        pass


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_make_composite_reference_designator(
        test_dao, test_configuration):
    """ request_do_make_composite_reference_designator() should return a zero error code on success. """
    DUT = dtcHardwareBoM(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(revision_id=1)

    (_error_code,
     _msg) = DUT.request_do_make_composite_reference_designator(node_id=1)

    assert _error_code == 0
    assert _msg == ''
    assert DUT.request_get_attributes(2)['comp_ref_des'] == 'S1:SS1'
